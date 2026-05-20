"""
Integration test for the PlantNet API service.
"""
import os
from requests_mock import ANY
from services.plantnet import identify_plant


def test_identify_plant_mocked(requests_mock):
    """Test the identify_plant function using a mocked API response."""
    image_path = "data/photos/guzmania_conifera.jpg"
    assert os.path.exists(image_path), f"Test image not found at {image_path}"

    fake_response = {
        "results": [
            {
                "score": 0.99,
                "species": {
                    "scientificNameWithoutAuthor": "Mocked guzmania_conifera"
                }
            }
        ]
    }

    # 2. Intercept the request. ANY catches all POST requests.
    requests_mock.post(ANY, json=fake_response, status_code=200)

    # 3. Call your function normally. It won't hit the real API.
    result = identify_plant(image_path, organ="flower")

    # 4. Assert the function correctly handled your fake data
    assert isinstance(result, dict)
    assert len(result["results"]) > 0

    top_match = result["results"][0]["species"]["scientificNameWithoutAuthor"]

    # We assert against our fake name to prove the mock worked
    assert top_match == "Mocked guzmania_conifera"
    print(f"\nTop match found: {top_match}")
