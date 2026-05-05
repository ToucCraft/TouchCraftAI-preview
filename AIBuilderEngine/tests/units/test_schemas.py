import pytest
from pydantic import ValidationError
from schemas.block_schemas import HeroBlock, FeaturesBlock


def test_hero_block_accepts_valid_data():
    """
    Test: Verify that a correctly formatted JSON (mocking valid AI response)
    is successfully parsed into a HeroBlock Pydantic model.
    """
    valid_payload = {
        "type": "hero",
        "props": {
            "title": "Welcome to our SaaS",
            "subtitle": "Build faster",
            "cta_text": "Get Started",
            "image_prompt": "Futuristic abstract background",
            "image_url": ""
        }
    }

    block = HeroBlock(**valid_payload)

    assert block.type == "hero"
    assert block.props.title == "Welcome to our SaaS"
    assert block.props.cta_text == "Get Started"


def test_features_block_rejects_ai_hallucination():
    """
    Test: Simulate an AI hallucination where it returns a string
    instead of a list of objects for the 'features' field.
    Expectation: Pydantic should raise a ValidationError.
    """
    hallucinated_payload = {
        "type": "features",
        "props": {
            "title": "Our Advantages",
            "features": "Fast, Secure, Scalable"  # AI Error: Should be List[FeatureItem]
        }
    }

    with pytest.raises(ValidationError) as exc_info:
        FeaturesBlock(**hallucinated_payload)

    # Assert that the error is specifically about the 'features' field type
    assert "Input should be a valid list" in str(exc_info.value)