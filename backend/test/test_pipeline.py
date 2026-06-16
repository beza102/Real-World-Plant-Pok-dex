"""
Integration test for the full identify → describe pipeline.
Verifies PlantNet's string return works with Gemini's generate_pokedex_entry.
"""
from requests_mock import ANY

from services.gemini_service import generate_pokedex_entry
from services.plantnet import identify_plant

FAKE_PLANT_RESPONSE = {
    "results": [
        {
            "score": 0.99,
            "species": {
                "scientificNameWithoutAuthor": "Guzmania conifera"
            }
        }
    ]
}

FAKE_ENTRY = (
    "Guzmania conifera thrives in tropical rainforests. "
    "Its bracts outlast many flowers. "
    "Care difficulty: Moderate — it needs bright indirect light."
)


def test_identify_then_describe_mocked(mocker, requests_mock):
    """PlantNet returns a string; Gemini accepts it and returns a full entry."""
    mocker.patch("services.plantnet.os.path.exists", return_value=True)
    mocker.patch("services.plantnet.os.path.getsize", return_value=1000)
    mocker.patch("services.plantnet.open", mocker.mock_open(read_data=b"fakeimagebytes"))
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)

    mock_response = mocker.Mock()
    mock_response.text = FAKE_ENTRY
    mock_client = mocker.Mock()
    mock_client.models.generate_content = mocker.Mock(return_value=mock_response)
    mocker.patch("services.gemini_service.genai.Client", return_value=mock_client)

    scientific_name = identify_plant("data/photos/guzmania_conifera.jpg", organ="flower")
    assert isinstance(scientific_name, str)

    result = generate_pokedex_entry(scientific_name)
    assert result["scientific_name"] == "Guzmania conifera"
    assert result["entry"] == FAKE_ENTRY
