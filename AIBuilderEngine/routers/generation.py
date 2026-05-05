import uuid
import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from pydantic import BaseModel
from google import genai
from google.genai import types
from typing import Optional, List

from core.database import get_db
from core.auth import get_current_user
from core.config import settings
from core.s3 import s3_client
from models import User, Project
from schemas.site_schema import SiteGenerationRequest
from services.generator import generate_site_structure
from services.image_gen import generate_and_upload_image

router = APIRouter()

class AssetGenRequest(BaseModel):
    asset_type: str
    prompt: Optional[str] = None
    existing_image: Optional[str] = None

@router.post("/generate", response_model=dict)
async def generate_draft(request: SiteGenerationRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        project_id = str(uuid.uuid4())
        site_data = generate_site_structure(request)
        site_dict = site_data.model_dump()
        site_dict['id'] = project_id

        new_project = Project(
            id=project_id, user_id=current_user.id, business_name=request.business_name,
            business_description=request.business_description,
            language=request.languages[0] if request.languages else "en",
            site_config=site_dict, status="draft",
            theme_color=site_dict.get('palette', {}).get('primary', '#000000')
        )
        db.add(new_project)
        db.commit()
        return {"project_id": project_id, "status": "draft", "preview_data": site_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{project_id}/upload-asset", response_model=dict)
async def upload_project_asset(project_id: str, asset_type: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project: raise HTTPException(404, "Project not found")

    file_content = await file.read()
    filename = f"custom_{asset_type}_{uuid.uuid4().hex[:6]}.png"
    s3_path = f"projects/{project_id}/uploads/{filename}"
    s3_url = s3_client.upload_file(file_content, s3_path, file.content_type or "image/png")

    current_config = dict(project.site_config)
    blocks = current_config.get('blocks', [])
    updated = False

    if asset_type == 'favicon':
        current_config['favicon'] = s3_url; updated = True
    elif asset_type == 'logo':
        current_config['logo_url'] = s3_url; updated = True
    else:
        for block in blocks:
            if asset_type in block.get('type', '').lower():
                if 'props' not in block: block['props'] = {}
                block['props']['image_url'] = s3_url
                updated = True; break

    if updated:
        project.site_config = current_config
        flag_modified(project, "site_config")
        db.commit()
        return {"url": s3_url, "status": "updated"}
    return {"url": s3_url, "status": "uploaded_only"}


@router.post("/{project_id}/generate-asset")
async def generate_project_asset(project_id: str, request: AssetGenRequest, db: Session = Depends(get_db)):
    asset_type = request.asset_type
    user_prompt = request.prompt

    project = db.query(Project).filter(Project.id == project_id).first()
    if not project: raise HTTPException(404)

    current_config = dict(project.site_config)
    blocks = current_config.get('blocks', [])
    palette = current_config.get('palette', {})

    updated = False
    image_url = ""

    if asset_type == 'favicon':
        prompt = user_prompt if user_prompt else f"Minimalist flat app icon for {project.business_name}"
        try:
            image_url = await generate_and_upload_image(prompt, project.business_name, f"projects/{project_id}/assets",
                                                        f"favicon_{uuid.uuid4().hex[:6]}.png", asset_type="favicon",
                                                        palette=palette, existing_image=request.existing_image)
        except Exception as e:
            raise HTTPException(500, f"AI Error: {str(e)}")
        current_config['favicon'] = image_url;
        updated = True

    elif asset_type == 'logo':
        prompt = user_prompt if user_prompt else f"Minimalist modern logo for {project.business_name}"
        try:
            image_url = await generate_and_upload_image(prompt, project.business_name, f"projects/{project_id}/assets",
                                                        f"logo_{uuid.uuid4().hex[:6]}.png", asset_type="logo",
                                                        palette=palette, existing_image=request.existing_image)
        except Exception as e:
            raise HTTPException(500, f"AI Error: {str(e)}")
        current_config['logo_url'] = image_url
        if current_config.get('logo_mode') == 'text':
            current_config['logo_mode'] = 'both'
        updated = True

    else:
        for index, block in enumerate(blocks):
            if asset_type in block.get('type', '').lower():
                prompt = user_prompt
                if not prompt:
                    prompt_data = block.get('props', {}).get('image_prompt', 'Professional image')
                    prompt = prompt_data.get('en', list(prompt_data.values())[
                        0] if prompt_data else 'Professional photo') if isinstance(prompt_data, dict) else str(
                        prompt_data)

                try:
                    image_url = await generate_and_upload_image(prompt, project.business_name,
                                                                f"projects/{project_id}/assets",
                                                                f"{asset_type}_{index}_{uuid.uuid4().hex[:6]}.png",
                                                                asset_type=asset_type, palette=palette, existing_image=request.existing_image)
                except Exception as e:
                    raise HTTPException(500, f"AI Error: {str(e)}")

                if 'props' not in block: block['props'] = {}
                block['props']['image_url'] = image_url
                updated = True
                break

    if updated:
        project.site_config = current_config
        flag_modified(project, "site_config")
        db.commit()
        return {"url": image_url}

    raise HTTPException(400, f"Block type '{asset_type}' not found.")

class ChatEditRequest(BaseModel):
    message: str

@router.post("/{project_id}/chat-edit")
async def ai_edit_project(project_id: str, request: ChatEditRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project: raise HTTPException(404, "Project not found")

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    edit_prompt = f"""You are an expert web designer. 
    Current JSON Config: {json.dumps(project.site_config)}
    User Request: "{request.message}"
    Task: Update the JSON. Return ONLY the updated valid JSON."""

    try:
        response = await client.aio.models.generate_content(
            model=settings.GEMINI_MODEL_FAST, contents=edit_prompt,
            config=types.GenerateContentConfig(temperature=0.2, response_mime_type="application/json")
        )
        new_config = json.loads(response.text)
        project.site_config = new_config
        flag_modified(project, "site_config")
        db.commit()
        return {"status": "success", "config": new_config}
    except Exception as e:
        print(f"AI Edit Crash: {str(e)}")
        raise HTTPException(500, "Failed to update site via AI")

@router.post("/{project_id}/generate-seo")
async def generate_project_seo(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project: raise HTTPException(404, "Project not found")

    translations = project.site_config.get('translations', {})
    langs = list(translations.keys()) if translations else ['en']

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)
    prompt = f"""
    Act as an Expert SEO Specialist.
    Business Name: "{project.business_name}"
    Description: "{project.business_description}"
    Target Languages: {", ".join(langs)}

    Generate highly optimized SEO meta tags (Title, Description, Keywords).
    Return ONLY a valid JSON object matching this exact structure:
    {{
      "title": {{ "en": "Optimized Title max 60 chars", "ru": "..." }},
      "description": {{ "en": "Optimized description max 160 chars...", "ru": "..." }},
      "keywords": {{ "en": "keyword1, keyword2, keyword3", "ru": "..." }}
    }}
    """
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL, contents=prompt,
            config=types.GenerateContentConfig(temperature=0.7, response_mime_type="application/json")
        )
        seo_data = json.loads(response.text)
        current_config = dict(project.site_config)
        current_config['seo'] = seo_data
        project.site_config = current_config
        flag_modified(project, "site_config")
        db.commit()

        return {"status": "success", "seo": seo_data}
    except Exception as e:
        raise HTTPException(500, f"AI SEO Error: {str(e)}")


class ProductTranslateRequest(BaseModel):
    product: dict
    source_lang: str
    target_langs: list[str]


@router.post("/{project_id}/translate-product")
async def translate_product(
        project_id: str,
        request: ProductTranslateRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(404, "Project not found or access denied")

    source_lang = request.source_lang
    target_langs = request.target_langs
    p = request.product

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    prompt = f"""
    Translate the following e-commerce product details from '{source_lang}' to the following target languages: {", ".join(target_langs)}.

    Original Content ({source_lang}):
    Title: {p.get('title', {}).get(source_lang, '')}
    Description: {p.get('description', {}).get(source_lang, '')}
    Category: {p.get('category', {}).get(source_lang, '')}

    Return ONLY a valid JSON object matching this exact structure containing the translations for the TARGET LANGUAGES ONLY:
    {{
      "title": {{ "{target_langs[0]}": "...", "other_lang": "..." }},
      "description": {{ "{target_langs[0]}": "...", "other_lang": "..." }},
      "category": {{ "{target_langs[0]}": "...", "other_lang": "..." }}
    }}
    """
    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL, contents=prompt,
            config=types.GenerateContentConfig(temperature=0.3, response_mime_type="application/json")
        )
        current_user.ai_generations_used += 1
        db.commit()

        return json.loads(response.text)
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"AI Translation Error: {str(e)}")


class ChatMessage(BaseModel):
    role: str
    text: str


class ChatEditRequest(BaseModel):
    messages: List[ChatMessage]


@router.post("/{project_id}/chat-edit-stream")
async def ai_edit_project_stream(project_id: str, request: ChatEditRequest, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project: raise HTTPException(404, "Project not found")

    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    history_text = ""
    for msg in request.messages[:-1]:
        role_name = "User" if msg.role == "user" else "AI"
        history_text += f"{role_name}: {msg.text}\n"

    current_request = request.messages[-1].text

    edit_prompt = f"""You are an expert web designer helping a user build their site iteratively.
    Current JSON Config: {json.dumps(project.site_config)}

    Chat History:
    {history_text}

    User Request: "{current_request}"

    Task Instructions:
    1. First, explain your thought process and what you are going to change based on the request. Be friendly and concise.
    2. Then, output the ENTIRE updated valid JSON configuration for the site.
    3. You MUST enclose the JSON strictly inside a markdown code block like this:
    ```json
    {{ "your": "json here" }}
    ```
    Do not add any text after the JSON block.
    """

    async def generate_stream():
        try:
            response = await client.aio.models.generate_content_stream(
                model=settings.GEMINI_MODEL_FAST,
                contents=edit_prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )

            full_response = ""
            async for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    yield chunk.text.encode('utf-8')
                    await asyncio.sleep(0.01)

            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', full_response, re.DOTALL)
            if json_match:
                new_config_str = json_match.group(1)
                try:
                    new_config = json.loads(new_config_str)
                    project.site_config = new_config
                    flag_modified(project, "site_config")
                    db.commit()
                except json.JSONDecodeError:
                    print("Failed to parse JSON from AI response on backend save.")

        except Exception as e:
            print(f"AI Stream Error: {str(e)}")
            yield f"\n\n[Error: {str(e)}]".encode('utf-8')

    return StreamingResponse(generate_stream(), media_type="text/plain")
