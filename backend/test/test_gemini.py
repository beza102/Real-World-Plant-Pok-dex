"""
Integration test for the Gemini brain service (Pokédex entry generation).
"""
import pytest
from services.gemini_service import generate_pokedex_entry


FAKE_ENTRY = (
    "Guzmania conifera thrives in tropical rainforests of Central and South America. "
    "Its vibrant bracts can last for months, outlasting many flowers. "
    "Care difficulty: Moderate — it needs bright indirect light and consistent humidity."
)


def test_generate_pokedex_entry_mocked(mocker):
    """Test generate_pokedex_entry using a mocked Gemini API response."""
    mock_response = mocker.Mock()
    mock_response.text = FAKE_ENTRY

    mock_client = mocker.Mock()
    mock_client.models.generate_content = mocker.Mock(return_value=mock_response)
    mocker.patch("services.gemini_service.genai.Client", return_value=mock_client)

    result = generate_pokedex_entry("Guzmania conifera")

    assert result["scientific_name"] == "Guzmania conifera"
    assert result["entry"] == FAKE_ENTRY
    assert result["model"] == "gemini-2.5-flash"
    mock_client.models.generate_content.assert_called_once()


def test_empty_scientific_name():
    """Test that empty plant names are rejected."""
    with pytest.raises(ValueError, match="scientific_name must be a non-empty string"):
        generate_pokedex_entry("")

    with pytest.raises(ValueError, match="scientific_name must be a non-empty string"):
        generate_pokedex_entry("   ")


def test_gemini_api_error(mocker):
    """Test that Gemini API errors are propagated."""
    mock_client = mocker.Mock()
    mock_client.models.generate_content = mocker.Mock(
        side_effect=Exception("API unavailable")
    )
    mocker.patch("services.gemini_service.genai.Client", return_value=mock_client)

    with pytest.raises(Exception, match="API unavailable"):
        generate_pokedex_entry("Monstera deliciosa")
