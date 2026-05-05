from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any, Union

class ContactDetails(BaseModel):
    legal_name: Optional[str] = None
    address: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    socials: Optional[Dict[str, str]] = Field(default_factory=dict)

class SiteGenerationRequest(BaseModel):
    business_name: str
    business_description: str
    niche: str
    languages: List[str] = ["en", "es"]
    sections: List[Literal[
        'hero', 'about', 'features', 'map', 'faq', 'contacts', 'form', 'gallery'
    ]] = ['hero', 'about', 'features', 'faq', 'map', 'contacts', 'form', 'gallery']

    contact_details: Optional[ContactDetails] = None

class ColorPalette(BaseModel):
    primary: str = "#3B82F6"
    secondary: str = "#10B981"
    background: str = "#FFFFFF"
    text: str = "#1F2937"

class LegalContent(BaseModel):
    privacy_policy: str
    terms_of_service: str
    cookie_policy: str

class GeneratedBlock(BaseModel):
    category: str
    type: str
    id: str
    props: Dict[str, Any]

class GeneratedSite(BaseModel):
    id: Optional[str] = None
    business_name: str
    header_type: str
    footer_type: str
    palette: Dict[str, str]
    font: str = "Inter"
    blocks: List[GeneratedBlock]
    translations: Dict[str, Dict[str, str]] = Field(default_factory=dict)
    contact: Optional[ContactDetails] = None
    logo_url: Optional[str] = ""
    logo_mode: str = "text"

    has_catalog: Optional[bool] = False
    products: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
