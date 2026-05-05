import pytest
import json
from unittest.mock import patch, MagicMock
from services.generator import generate_site_structure
from schemas.site_schema import SiteGenerationRequest

MOCK_AI_JSON_RESPONSE = {
    "business_name": "Test SaaS",
    "header_type": "standard",
    "footer_type": "Footer",
    "palette": {"primary": "#000", "secondary": "#111", "background": "#fff", "text": "#333"},
    "theme_color": "#112233",
    "blocks": [],
    "translations": {"en": {"search": "Search"}}
}

@patch('services.generator.genai.Client')
def test_generate_site_structure_success(mock_genai_client_class):
    """
    Test: Verify that the generator correctly calls the Gemini API,
    parses the JSON response, and returns a valid GeneratedSite Pydantic object.
    """
    # Setup Mock for Google GenAI SDK
    mock_client_instance = MagicMock()
    mock_response = MagicMock()
    mock_response.text = json.dumps(MOCK_AI_JSON_RESPONSE)
    mock_client_instance.models.generate_content.return_value = mock_response
    mock_genai_client_class.return_value = mock_client_instance

    # Create mock request DTO
    request_dto = SiteGenerationRequest(
        business_name="Test SaaS",
        business_description="Testing platform",
        niche="Technology",
        languages=["en"],
        sections=["hero"]
    )

    # Execute service
    result = generate_site_structure(request_dto)

    # Assertions
    assert result.business_name == "Test SaaS"
    assert result.palette["primary"] == "#000"

    # Verify that the Gemini SDK was called exactly once
    mock_client_instance.models.generate_content.assert_called_once()
