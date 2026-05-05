import json
import os
from google import genai
from google.genai import types
from schemas.site_schema import GeneratedSite, SiteGenerationRequest
from core.config import settings

COMPONENT_LIBRARY = {
    "blocks": {
        "HeroBlock": ["title", "subtitle", "cta_text", "image_prompt"],
        "FeaturesBlock": ["title", "features: list of {title, description, icon (FontAwesome class string ONLY, e.g. 'fas fa-bolt')}"],
        "MapBlock": ["title", "address", "location_text"],
        "AboutBlock": ["title", "description", "image_prompt"],
        "FaqBlock": ["title", "faqs: list of {question, answer}"],
        "ContactBlock": ["title", "phone", "email", "address"],
        "FormBlock": ["title", "subtitle", "submit_button_text", "fields: list of {name, label, type, required, enabled}"],
        "GalleryBlock": ["title", "description"],
    },
    "headers": ["Header"],
    "footers": ["Footer"]
}


def generate_site_structure(request: SiteGenerationRequest) -> GeneratedSite:
    client = genai.Client(api_key=settings.GOOGLE_API_KEY)

    langs = request.languages if request.languages else ["en"]
    main_lang = langs[0]

    requested_sections = list(set(request.sections.copy()))

    include_catalog = 'catalog' in requested_sections

    block_sections = [s for s in requested_sections if s != 'catalog']

    example_translation = {lang: "..." for lang in langs}

    blocks_example = f"""
        {{
          "category": "blocks",
          "type": "HeroBlock",
          "id": "hero_1",
          "props": {{
            "title": {json.dumps(example_translation)},
            "subtitle": {json.dumps(example_translation)},
            "cta_text": {json.dumps(example_translation)},
            "image_prompt": "English description for AI image"
          }}
        }}"""

    if 'form' in requested_sections:
        blocks_example += f""",
        {{
          "category": "blocks",
          "type": "FormBlock",
          "id": "form_1",
          "props": {{
            "title": {json.dumps(example_translation)},
            "subtitle": {json.dumps(example_translation)},
            "submit_button_text": {json.dumps(example_translation)},
            "fields": [
               {{ "name": "name", "label": {json.dumps(example_translation)}, "type": "text", "required": true, "enabled": true }}
            ]
          }}
        }}"""

    form_instruction = " (Use FormBlock for lead generation)" if 'form' in requested_sections else ""

    REQUIRED_UI_KEYS = [
        "Home", "Features", "About", "FAQ", "Contact Us", "footer_desc",
        "Privacy Policy", "privacy_policy_text", "cookie_title", "cookie_text",
        "accept", "reject", "read_more", "quick_links", "follow_us", "all_rights_reserved",
        "form_subtitle", "form_leave_empty", "form_math_question", "form_math_error",
        "form_sending", "form_submit", "form_success", "form_error",
        "search_placeholder", "all_categories", "no_products_found", "Catalog"
    ]

    prompt = f"""
    Act as a Senior Web Architect. Generate a professional website structure in JSON.
    Business: "{request.business_name}" ({request.niche}). 
    Description: "{request.business_description}"
    Target Languages: {", ".join(langs)}
    Required Sections to Include: {", ".join(requested_sections)}{form_instruction}.

    COMPONENT LIBRARY & EXPECTED PROPS:
    {json.dumps(COMPONENT_LIBRARY, indent=2)}
    
    REQUIRED UI TRANSLATION KEYS (CHECKLIST):
    {json.dumps(REQUIRED_UI_KEYS)}

    STRICT RULES:
    1. EVERY text field must be an object with keys for ALL target languages: {langs}.
    2. Navigation & Footer keys MUST be inside "translations".
    3. STRICT COMPONENT NAMES: Use EXACTLY "FaqBlock" (not FAQBlock), "HeroBlock", "FormBlock", etc.
    4. Use these contact details for ContactBlock and Footer: {json.dumps(request.contact_details.model_dump() if request.contact_details else "Generate dummy data")}
    5. PRIVACY POLICY (GDPR COMPLIANT): For "privacy_policy_text", generate a detailed privacy policy for {request.business_name}. 
    YOU MUST INCLUDE THESE EXACT 7 SECTIONS using <h4> tags:
    <h4>1. Information We Collect</h4><p>...</p>
    <h4>2. How We Use Your Information</h4><p>...</p>
    <h4>3. Data Security and Sharing</h4><p>...</p>
    <h4>4. Cookies</h4><p>...</p>
    <h4>5. Your Rights</h4><p>...</p>
    <h4>6. Changes to This Policy</h4><p>...</p>
    <h4>7. Contact Us</h4><p>...</p>
    MUST BE VALID HTML ONLY (use <p>, <h4>, <ul>, <li>). ABSOLUTELY NO MARKDOWN (no ** or ##). Insert their email ({request.contact_details.email if request.contact_details else 'provided email'}) in the Contact Us section.
    6. YOU MUST INCLUDE BLOCKS FOR ALL REQUIRED SECTIONS: {", ".join(block_sections)}.
    7. DO NOT GENERATE BLOCKS THAT WERE NOT REQUESTED. DO NOT generate a Catalog block.
    8. For icons (like in FeaturesBlock), Output ONLY the raw FontAwesome class string (e.g., "fas fa-bolt").
    9. CRITICAL TRANSLATIONS: You MUST strictly generate translated strings for 'search_placeholder', 'all_categories', 'no_products_found', and 'Catalog' for ALL target languages in the "translations" dictionary. Do NOT skip them under ANY circumstances, even if no products or catalog blocks are requested.
    10. CRITICAL RULE REGARDING FORMS: The user has requested EXACTLY these sections: {", ".join(requested_sections)}. You MUST ONLY generate blocks that map to these requested sections. Under NO CIRCUMSTANCES should you generate a 'FormBlock' or any lead capture forms UNLESS 'form' is explicitly included in the requested sections list. If 'form' is not in the list, DO NOT include a FormBlock.
    JSON EXAMPLE FORMAT TO FOLLOW:
    {{
      "business_name": "string",
      "has_catalog": {str(include_catalog).lower()},
      "header_type": "Header",
      "footer_type": "Footer",
      "palette": {{ "primary": "#3B82F6", "secondary": "#10B981", "background": "#FFFFFF", "text": "#1F2937" }},
      "blocks": [
        {blocks_example}
      ],
      "translations": {{
        "{main_lang}": {{
          "Home": "...",
          "Features": "...",
          "About": "...",
          "FAQ": "...",
          "Contact Us": "...",
          "footer_desc": "...",
          "Privacy Policy": "...",
          "privacy_policy_text": "<h4>1. Information We Collect</h4><p>...</p>",
          "cookie_title": "Cookies & Privacy",
          "cookie_text": "We use cookies to enhance your experience. By continuing to visit this site you agree to our use of cookies and Privacy Policy.",
          "accept": "Accept All",
          "reject": "Decline",
          "read_more": "...",
          "quick_links": "...", 
          "follow_us": "...",
          "all_rights_reserved": "...",
          "form_subtitle": "Please fill out the form below, and we will get back to you shortly.",
          "form_leave_empty": "Leave this field empty",
          "form_math_question": "How much is",
          "form_math_error": "Incorrect answer, please try again.",
          "form_sending": "Sending...",
          "form_submit": "Submit",
          "form_success": "Thank you! Your message has been sent successfully.",
          "form_error": "An error occurred while sending. Please try again later.",
          "search_placeholder": "Search products...",
          "all_categories": "All Categories",
          "no_products_found": "No products found",
          "Catalog": "Our Catalog"
        }},
        "other_langs": "Generate exactly the same keys for ALL requested target languages..."
      }},
      "contact": {{
        "email": "...",
        "phone": "...",
        "address": "...",
        "socials": {{ "instagram": "url" }}
      }}
    }}
    """

    try:
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                response_mime_type="application/json"
            )
        )

        if response.text:
            data = json.loads(response.text)
            if request.contact_details:
                data['contact'] = request.contact_details.model_dump()
            return GeneratedSite(**data)
        raise Exception("Gemini returned empty text")
    except Exception as e:
        print(f"❌ Generation Error: {e}")
        raise e
