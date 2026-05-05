from pydantic import BaseModel, Field
from typing import Literal, List, Union

class BaseBlock(BaseModel):
    type: str

class HeroBlockProps(BaseModel):
    title: str
    subtitle: str
    cta_text: str
    variant: str = "center"
    image_prompt: str
    image_url: str = ""

class HeroBlock(BaseBlock):
    type: Literal['hero'] = 'hero'
    props: HeroBlockProps

class FeatureItem(BaseModel):
    title: str
    description: str
    icon: str

class FeaturesBlockProps(BaseModel):
    title: str
    features: List[FeatureItem]

class FeaturesBlock(BaseBlock):
    type: Literal['features'] = 'features'
    props: FeaturesBlockProps

class MapBlockProps(BaseModel):
    title: str = "Visit Us"
    location_text: str = "Our Location"
    address: str
    lat: float = 0.0
    lng: float = 0.0

class MapBlock(BaseBlock):
    type: Literal['map'] = 'map'
    props: MapBlockProps

class AboutBlockProps(BaseModel):
    title: str
    description: str
    image_url: str = ""

class AboutBlock(BaseBlock):
    type: Literal['about'] = 'about'
    props: AboutBlockProps

class FaqItem(BaseModel):
    question: str
    answer: str

class FaqBlockProps(BaseModel):
    title: str
    faqs: List[FaqItem]

class FaqBlock(BaseBlock):
    type: Literal['faq'] = 'faq'
    props: FaqBlockProps

class ContactBlockProps(BaseModel):
    title: str
    email: str
    phone: str
    address: str

class ContactBlock(BaseBlock):
    type: Literal['contacts'] = 'contacts'
    props: ContactBlockProps


class FormField(BaseModel):
    name: str
    label: str
    type: Literal['text', 'email', 'phone', 'textarea']
    required: bool = False
    enabled: bool = True


class FormBlockProps(BaseModel):
    title: str = "Contact Us"
    subtitle: str = "We will contact you as soon as posible"
    submit_button_text: str = "Send"

    fields: List[FormField] = [
        FormField(name="name", label="Name", type="text", required=True, enabled=True),
        FormField(name="phone", label="Phone", type="phone", required=True, enabled=True),
        FormField(name="email", label="Email", type="email", required=False, enabled=False),
        FormField(name="message", label="Message", type="textarea", required=False, enabled=True),
    ]


class FormBlock(BaseBlock):
    type: Literal['form'] = 'form'
    props: FormBlockProps


class GalleryBlockProps(BaseModel):
    title: str
    description: str = ""
    images: List[str] = Field(default_factory=list)

class GalleryBlock(BaseBlock):
    type: Literal['gallery'] = 'gallery'
    props: GalleryBlockProps

# --- Union ---
BlockType = Union[HeroBlock, FeaturesBlock, MapBlock, AboutBlock, FaqBlock, ContactBlock, FormBlock, GalleryBlock]