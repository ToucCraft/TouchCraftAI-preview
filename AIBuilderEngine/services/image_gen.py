from google import genai
from google.genai import types
from core.config import settings
from core.s3 import s3_client
import requests
from io import BytesIO


async def generate_and_upload_image(
        prompt: str,
        business_name: str,
        folder_path: str,
        file_name: str,
        asset_type: str = "hero",
        palette: dict = None,
        existing_image: str = None
) -> str:
    if not prompt or not prompt.strip():
        print(f"⚠️ Warning: empty prompt for {asset_type}. fallback.")
        prompt = f"Abstract background representing the core services of '{business_name}'"

    model_name = settings.IMAGE_MODEL
    print(f"🎨 Generating {file_name} ({asset_type}) in {folder_path} using {model_name}...")

    color_hint = ""
    if palette:
        color_hint = f" Incorporate subtle accents of these hex colors to match the brand: primary {palette.get('primary', '')} and secondary {palette.get('secondary', '')}."

    if asset_type == "favicon":
        ai_prompt = f"Minimalist logo icon for {business_name}. {prompt}.{color_hint} Vector style, flat design, simple shape, white background, high contrast, app icon style."
        ratio = "1:1"
        placeholder_size = "512x512"
    elif asset_type == "logo":
        ai_prompt = f"Professional clean minimalist logo for {business_name}. {prompt}.{color_hint} Isolated on a pure solid tranparent background. Vector art style, flat design, highly scalable, elegant."
        ratio = "1:1"
        placeholder_size = "512x512"
    else:
        ai_prompt = f"{prompt}. {color_hint}".strip()
        ratio = "16:9"
        placeholder_size = "1024x600"

    try:
        client = genai.Client(api_key=settings.GOOGLE_API_KEY)

        if existing_image:
            print(f"🔄 Fetching existing image for editing: {existing_image}")
            try:
                img_resp = requests.get(existing_image, timeout=10)
                img_resp.raise_for_status()
                base_image_bytes = img_resp.content

                print("✨ Edit with Vertex AI...")

                vertex_client = genai.Client(
                    vertexai=True,
                    project=settings.GCP_PROJECT_ID,
                    location=settings.GCP_LOCATION
                )

                from google.genai.types import RawReferenceImage, EditImageConfig

                raw_ref = RawReferenceImage(
                    reference_image=types.Image(image_bytes=base_image_bytes),
                    reference_id=1
                )

                response = vertex_client.models.edit_image(
                    model="imagen-4.0-generate-001",
                    prompt=ai_prompt,
                    reference_images=[raw_ref],
                    config=EditImageConfig(number_of_images=1)
                )

                image_bytes = response.generated_images[0].image.image_bytes
                s3_url = s3_client.upload_file(image_bytes, f"{folder_path}/{file_name}", content_type="image/png")

                print(f"✅ Saved edited image: {s3_url}")
                return s3_url

            except Exception as e:
                print(f"⚠️ Failed to edit existing image, falling back to basic generation: {e}")

        print("✨ Generate again...")
        response = client.models.generate_images(
            model=model_name,
            prompt=ai_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio=ratio,
                person_generation="allow_adult"
            )
        )

        if not response.generated_images:
            raise Exception("No image returned from Google AI")

        image_bytes = response.generated_images[0].image.image_bytes
        s3_url = s3_client.upload_file(image_bytes, f"{folder_path}/{file_name}", content_type="image/png")

        print(f"✅ Saved: {s3_url}")
        return s3_url

    except Exception as e:
        print(f"❌ Image Gen Failed: {e}")
        return f"https://placehold.co/{placeholder_size}?text={file_name.replace('.png', '')}"
