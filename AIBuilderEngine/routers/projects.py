import subprocess
import socket
from typing import List as ListType, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified

from core.database import get_db
from core.auth import get_current_user
from core.config import settings
from models import User, Project
from services.npm_manager import NPMManager
from sync_domains import sync_db_with_npm
from services.template_gen import generate_project_files
from services.deployer import deploy_client_site, stop_container, start_container
from core.s3 import s3_client

router = APIRouter()

@router.get("/list", response_model=ListType[Dict[str, Any]])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.user_id == current_user.id).order_by(Project.created_at.desc()).all()
    result = []
    for p in projects:
        thumbnail_url = None
        if p.site_config and "blocks" in p.site_config:
            for block in p.site_config["blocks"]:
                cat = block.get("category", "").lower()
                typ = block.get("type", "").lower()
                if cat == "hero" or typ.startswith("hero"):
                    thumbnail_url = block.get("props", {}).get("image_url")
                    break
        result.append({
            "id": p.id, "name": p.business_name, "status": p.status,
            "url": p.preview_url,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M"), "thumbnail": thumbnail_url
        })
    return result

@router.get("/{project_id}/logs")
def get_project_logs(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project or not project.container_id:
        raise HTTPException(404, "Active container not found.")
    try:
        result = subprocess.check_output(["docker", "logs", "--tail", "50", project.container_id], stderr=subprocess.STDOUT)
        return {"logs": result.decode("utf-8")}
    except Exception as e:
        return {"logs": f"Error: {str(e)}"}

@router.get("/{project_id}", response_model=dict)
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project: raise HTTPException(404, "Project not found")
    return {"id": project.id, "business_name": project.business_name, "status": project.status, "url": project.preview_url, "config": project.site_config}

@router.patch("/{project_id}", response_model=dict)
async def update_project(project_id: str, updates: Dict[str, Any], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project: raise HTTPException(404, "Access denied")
    if "site_config" in updates:
        new_conf = updates["site_config"]
        new_conf['id'] = project_id
        project.site_config = new_conf
        flag_modified(project, "site_config")
    db.commit()
    return {"message": "Updated"}

TIER_LIMITS = {
    "freemium": 1,
    "starter": 5,
    "pro": 10
}

@router.post("/{project_id}/deploy", response_model=dict)
async def deploy_project(project_id: str, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(404, "Project not found or access denied")

    tier = (current_user.subscription_tier or "freemium").lower()
    max_active_sites = TIER_LIMITS.get(tier, 1)

    active_count = db.query(Project).filter(Project.user_id == current_user.id, Project.status == "active").count()

    if active_count >= max_active_sites:
        raise HTTPException(403,
                            f"Limit reached: Your {tier} plan allows maximum {max_active_sites} active sites. Please stop another site first.")

    try:
        project.status = "building"
        db.commit()

        generated_files = generate_project_files(project.site_config)
        project_folder = f"projects/{project_id}"
        for file_path, content in generated_files.items():
            s3_client.upload_file(content.encode('utf-8'), f"{project_folder}/{file_path}")

        deploy_client_site(project_id)

        project.status = "active"
        project.container_id = f"container-{project_id}"

        existing_url = project.preview_url or ""
        is_custom_domain = bool(existing_url) and "localhost" not in existing_url

        if not is_custom_domain:
            auto_domain = f"{project_id}.touchcraftai.com"
            npm = NPMManager(settings.NPM_API_URL, settings.NPM_EMAIL, settings.NPM_PASSWORD)
            npm_res = npm.create_proxy_host(auto_domain, project.container_id, port=80)
            project.preview_url = f"https://{auto_domain}" if npm_res else f"http://{auto_domain}"
            if npm_res:
                try:
                    sync_db_with_npm()
                except:
                    pass

        db.commit()
        return {"url": project.preview_url, "status": "active"}
    except Exception as e:
        project.status = "error"
        db.commit()
        raise HTTPException(500, f"Deploy failed: {str(e)}")


@router.post("/{project_id}/stop", response_model=dict)
async def stop_project(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project: raise HTTPException(404, "Access denied")

    try:
        stop_container(project_id)
        project.status = "stopped"
        db.commit()
        return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(500, f"Failed to stop container: {str(e)}")


@router.post("/{project_id}/start", response_model=dict)
async def start_project(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project:
        raise HTTPException(404, "Access denied")

    tier = (current_user.subscription_tier or "freemium").lower()
    max_active_sites = TIER_LIMITS.get(tier, 1)

    active_count = db.query(Project).filter(Project.user_id == current_user.id, Project.status == "active").count()

    if active_count >= max_active_sites:
        raise HTTPException(403,
                            f"Limit reached: Your {tier} plan allows maximum {max_active_sites} active sites. Please stop another site first.")

    try:
        start_container(project_id)
        project.status = "active"
        db.commit()
        return {"status": "active"}
    except Exception as e:
        raise HTTPException(500, f"Failed to start container: {str(e)}")

@router.post("/{project_id}/setup-domain")
async def setup_custom_domain(project_id: str, domain: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project: raise HTTPException(404, "Access denied")

    clean_domain = domain.replace("https://", "").replace("http://", "").rstrip("/")
    try:
        target_ip = socket.gethostbyname(clean_domain)
        if target_ip != "217.160.204.89": raise HTTPException(400, "Set A-record to 217.160.204.89")
    except socket.gaierror:
        raise HTTPException(400, "DNS Error")

    npm = NPMManager(settings.NPM_API_URL, settings.NPM_EMAIL, settings.NPM_PASSWORD)
    if npm.create_proxy_host(clean_domain, f"container-{project_id}", port=80):
        project.preview_url = f"https://{clean_domain}"
        db.commit()
        try: sync_db_with_npm()
        except: pass
        return {"status": "active", "url": project.preview_url}
    raise HTTPException(500, "NPM API error.")

@router.delete("/{project_id}", response_model=dict)
async def delete_project(project_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.user_id == current_user.id).first()
    if not project: raise HTTPException(404, "Access denied")
    try:
        subprocess.run(["docker", "rm", "-f", f"container-{project_id}"], capture_output=True)
        db.delete(project)
        db.commit()
        return {"status": "deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))
