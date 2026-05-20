"""
Integration test for the PlantNet API service.
"""
import os
import pytest
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

    requests_mock.post(ANY, json=fake_response, status_code=200)
    result = identify_plant(image_path, organ="flower")

    assert isinstance(result, dict)
    assert len(result["results"]) > 0
    top_match = result["results"][0]["species"]["scientificNameWithoutAuthor"]
    assert top_match == "Mocked guzmania_conifera"
    print(f"\nTop match found: {top_match}")


def test_invalid_file_format(mocker):
    """Test that invalid file formats are rejected."""
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    with pytest.raises(ValueError, match="Invalid file format"):
        identify_plant("data/photos/plant.gif")

    with pytest.raises(ValueError, match="Invalid file format"):
        identify_plant("data/photos/plant.txt")


def test_valid_jpg_format(requests_mock):
    """Test that .jpg files are accepted."""
    image_path = "data/photos/guzmania_conifera.jpg"
    fake_response = {"results": []}
    requests_mock.post(ANY, json=fake_response, status_code=200)
    result = identify_plant(image_path)
    assert isinstance(result, dict)


def test_valid_png_format(mocker, requests_mock):
    """Test that .png files are accepted."""
    image_path = "data/photos/guzmania_conifera.png"
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    mocker.patch('services.plantnet.os.path.getsize', return_value=1000)
    mocker.patch('services.plantnet.open', mocker.mock_open())
    fake_response = {"results": []}
    requests_mock.post(ANY, json=fake_response, status_code=200)
    result = identify_plant(image_path)
    assert isinstance(result, dict)


def test_valid_jpeg_format(mocker, requests_mock):
    """Test that .jpeg files are accepted."""
    image_path = "data/photos/guzmania_conifera.jpeg"
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    mocker.patch('services.plantnet.os.path.getsize', return_value=1000)
    mocker.patch('services.plantnet.open', mocker.mock_open())
    fake_response = {"results": []}
    requests_mock.post(ANY, json=fake_response, status_code=200)
    result = identify_plant(image_path)
    assert isinstance(result, dict)


def test_file_too_large(mocker):
    """Test that files exceeding 50 MB are rejected."""
    image_path = "data/photos/guzmania_conifera.jpg"
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    mocker.patch('services.plantnet.os.path.getsize', return_value=52428800 + 1)
    with pytest.raises(ValueError, match="File too large"):
        identify_plant(image_path)


def test_file_exactly_at_size_limit(mocker):
    """Test that files at exactly 50 MB are accepted."""
    image_path = "data/photos/guzmania_conifera.jpg"
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    mocker.patch('services.plantnet.os.path.getsize', return_value=52428800)
    mocker.patch('services.plantnet.open', mocker.mock_open())
    mock_response = mocker.patch('services.plantnet.requests.post')
    mock_response.return_value.json.return_value = {"results": []}
    result = identify_plant(image_path)
    assert isinstance(result, dict)


def test_nonexistent_file():
    """Test that nonexistent files are rejected."""
    with pytest.raises(FileNotFoundError):
        identify_plant("data/photos/nonexistent_plant.jpg")


def test_file_without_extension(mocker):
    """Test that files without extensions are rejected."""
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    with pytest.raises(ValueError, match="Invalid file format"):
        identify_plant("data/photos/guzmania_conifera")


def test_uppercase_extension(mocker):
    """Test that uppercase extensions are accepted (converted to lowercase)."""
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    mocker.patch('services.plantnet.os.path.getsize', return_value=1000)
    mocker.patch('services.plantnet.open', mocker.mock_open())
    mock_response = mocker.patch('services.plantnet.requests.post')
    mock_response.return_value.json.return_value = {"results": []}
    result = identify_plant("data/photos/guzmania_conifera.JPG")
    assert isinstance(result, dict)


def test_more_invalid_extensions(mocker):
    """Test that various invalid extensions are rejected."""
    mocker.patch('services.plantnet.os.path.exists', return_value=True)
    invalid_extensions = ["pdf", "doc", "zip", "exe", "mp4", "webp", "bmp"]
    for ext in invalid_extensions:
        with pytest.raises(ValueError, match="Invalid file format"):
            identify_plant(f"data/photos/guzmania_conifera.{ext}")
