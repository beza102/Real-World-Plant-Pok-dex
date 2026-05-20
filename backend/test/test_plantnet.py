"""This test verifies the functionality of the plant identification service using PlantNet API"""
import os
from services.plantnet import identify_plant

def test_identify_plant_with_real_api():
    """Test identification of a plant using the real PlantNet API."""
    # Updated path to match your folder structure
    image_path = "data/photos/guzmania_conifera.jpg"

    # ... rest of your test code remains exactly the same
    assert os.path.exists(image_path), f"Test image not found at {image_path}"
    result = identify_plant(image_path)

    assert isinstance(result, dict), "Expected the response to be a dictionary"
    assert "results" in result, "Expected 'results' key in the API response"
    assert len(result["results"]) > 0, "Expected at least one plant identification result"

    top_match = result["results"][0]["species"]["scientificNameWithoutAuthor"]
    print(f"\nTop match found: {top_match}")
