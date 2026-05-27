"""
Integration test for the PlantNet API service.
"""
import pytest
from requests_mock import ANY
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

@pytest.fixture
def mock_image(mocker):
    """Mock filesystem calls to avoid hitting disk."""
    mocker.patch("services.plantnet.os.path.exists", return_value=True)
    mocker.patch("services.plantnet.os.path.getsize", return_value=1000)
    mocker.patch("services.plantnet.open", mocker.mock_open(read_data=b"fakeimagebytes"))


@pytest.mark.usefixtures("mock_image")
def test_identify_plant_mocked(requests_mock):
    """Test the identify_plant function using a mocked API response."""
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)
    plant = identify_plant("fake/plant.jpg", organ="flower")
    assert isinstance(plant, str)
    assert plant == "Guzmania conifera"
    print(f"\nTop match found: {plant}")


def test_invalid_file_format(mocker):
    """Test that invalid file formats are rejected."""
    mocker.patch("services.plantnet.os.path.exists", return_value=True)
    with pytest.raises(ValueError, match="Invalid file format"):
        identify_plant("fake/plant.gif")
    with pytest.raises(ValueError, match="Invalid file format"):
        identify_plant("fake/plant.txt")


@pytest.mark.usefixtures("mock_image")
def test_valid_jpg_format(requests_mock):
    """Test that .jpg files are accepted."""
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)
    plant = identify_plant("fake/plant.jpg")
    assert isinstance(plant, str)


@pytest.mark.usefixtures("mock_image")
def test_valid_png_format(requests_mock):
    """Test that .png files are accepted."""
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)
    plant = identify_plant("fake/plant.png")
    assert isinstance(plant, str)


@pytest.mark.usefixtures("mock_image")
def test_valid_jpeg_format(requests_mock):
    """Test that .jpeg files are accepted."""
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)
    result = identify_plant("fake/plant.jpeg")
    assert isinstance(result, str)


def test_file_too_large(mocker):
    """Test that files exceeding 50 MB are rejected."""
    mocker.patch("services.plantnet.os.path.exists", return_value=True)
    mocker.patch("services.plantnet.os.path.getsize", return_value=52428800 + 1)
    with pytest.raises(ValueError, match="File too large"):
        identify_plant("fake/plant.jpg")


@pytest.mark.usefixtures("mock_image")
def test_file_exactly_at_size_limit(mocker, requests_mock):
    """Test that files at exactly 50 MB are accepted."""
    mocker.patch("services.plantnet.os.path.getsize", return_value=52428800)
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)
    plant = identify_plant("fake/plant.jpg")
    assert isinstance(plant, str)
    assert plant == "Guzmania conifera"


def test_nonexistent_file(mocker):
    """Test that nonexistent files are rejected."""
    mocker.patch("services.plantnet.os.path.exists", return_value=False)
    with pytest.raises(FileNotFoundError):
        identify_plant("fake/nonexistent.jpg")


def test_file_without_extension(mocker):
    """Test that files without extensions are rejected."""
    mocker.patch("services.plantnet.os.path.exists", return_value=True)
    with pytest.raises(ValueError, match="Invalid file format"):
        identify_plant("fake/plant")


@pytest.mark.usefixtures("mock_image")
def test_uppercase_extension(requests_mock):
    """Test that uppercase extensions are accepted (converted to lowercase)."""
    requests_mock.post(ANY, json=FAKE_PLANT_RESPONSE, status_code=200)
    plant = identify_plant("fake/plant.JPG")
    assert isinstance(plant, str)
    assert plant == "Guzmania conifera"


def test_more_invalid_extensions(mocker):
    """Test that various invalid extensions are rejected."""
    mocker.patch("services.plantnet.os.path.exists", return_value=True)
    invalid_extensions = ["pdf", "doc", "zip", "exe", "mp4", "webp", "bmp"]
    for ext in invalid_extensions:
        with pytest.raises(ValueError, match="Invalid file format"):
            identify_plant(f"fake/plant.{ext}")
