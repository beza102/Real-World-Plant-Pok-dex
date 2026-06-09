"""
Service module for interacting with the PlantNet API.
Handles image validation and plant identification requests.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

PLANTNET_API_KEY = os.getenv('PLANTNET_API_KEY')
PLANTNET_API_URL = "https://my-api.plantnet.org/v2/identify/all"

def identify_plant(image_path, organ="auto"):
    """
    Identify a plant from an image file.
    
    Args:
        image_path (str): Path to the image file (e.g., 'backend/data/photos/plant.jpg')
        organ (str): Plant organ type - 'leaf', 'flower', 'fruit', 'bark', or 'auto'
    
    Returns:
        str: Scientific name of the identified plant species.
    """
    # Check if file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Check file format
    valid_extensions = {'.jpg', '.jpeg', '.png'}
    file_ext = os.path.splitext(image_path)[1].lower()
    if file_ext not in valid_extensions:
        raise ValueError(f"Invalid file format: {file_ext}. Expected jpg or png")

    # Check file size (50 MB limit)
    file_size = os.path.getsize(image_path)
    max_size = 52428800  # 50 MB in bytes
    if file_size > max_size:
        raise ValueError(f"File too large: {file_size} bytes (max: {max_size})")

    # Prepare the request
    url = f"{PLANTNET_API_URL}?api-key={PLANTNET_API_KEY}"

    # Open and send the image
    with open(image_path, 'rb') as image_file:
        files = {
            'images': image_file
        }
        data = {
            'organs': organ
        }

        try:
            response = requests.post(url, files=files, data=data, timeout=10)
            response.raise_for_status()  # Raise error for bad status codes
            json_response = response.json()
            return json_response["results"][0]["species"]["scientificNameWithoutAuthor"]

        except requests.exceptions.RequestException as e:
            print(f"Error calling PlantNet API: {e}")
            raise


if __name__ == "__main__":
    image_path = "data/photos/guzmania_conifera.jpg"
    scientific_name = identify_plant(image_path, organ="flower")
    print(f"Identified: {scientific_name}")
