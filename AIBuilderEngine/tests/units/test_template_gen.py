import pytest
from services.template_gen import flatten_for_lang


def test_flatten_for_lang_extracts_target_language():
    """
    Test: Verify that the localization algorithm correctly extracts
    the target language (e.g., 'es') from a nested multilingual JSON structure.
    """
    multilingual_data = {
        "business_name": "Global Tech",
        "blocks": [
            {
                "type": "hero",
                "props": {
                    "title": {"en": "Hello", "es": "Hola", "uk": "Привіт"},
                    "items": [
                        {"desc": {"en": "Fast", "es": "Rápido"}}
                    ]
                }
            }
        ]
    }

    spanish_result = flatten_for_lang(multilingual_data, lang="es")

    # Assert that string primitives are untouched
    assert spanish_result["business_name"] == "Global Tech"

    # Assert that language objects are flattened to strings
    assert spanish_result["blocks"][0]["props"]["title"] == "Hola"
    assert spanish_result["blocks"][0]["props"]["items"][0]["desc"] == "Rápido"


def test_flatten_for_lang_uses_fallback():
    """
    Test: Verify that the algorithm falls back to English ('en')
    if the requested language is missing in the AI response.
    """
    incomplete_data = {
        "title": {"en": "Only English Available", "es": "Solo Español"}
    }

    # Requesting Ukrainian, which doesn't exist. Should fallback to English.
    result = flatten_for_lang(incomplete_data, lang="uk", fallback="en")

    assert result["title"] == "Only English Available"
