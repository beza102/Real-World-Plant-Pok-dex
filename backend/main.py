"""
main.py — FastAPI backend for the Real-World Plant Pokédex
Connects the frontend to PlantNet (plant ID) and Gemini (Pokédex entry).
"""

import os
import uuid
import tempfile

import requests as http_requests
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from services.plantnet import identify_plant
from services.gemini_service import generate_pokedex_entry

app = FastAPI()

# Allow the React frontend (running on localhost:5173) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Plant Pokédex backend is running."}


@app.post("/identify")
async def identify(file: UploadFile = File(...)):
    """
    Accepts an uploaded image, runs it through PlantNet to get the plant name,
    then passes that name to Gemini to generate a Pokédex entry.
    """

    # 1. Validate file type
    if file.content_type not in ("image/jpeg", "image/png"):
        raise HTTPException(
            status_code=400,
            detail="Only JPG and PNG images are supported."
        )

    # 2. Save the uploaded file to a temp location so PlantNet can read it
    suffix = ".jpg" if file.content_type == "image/jpeg" else ".png"
    tmp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}{suffix}")

    try:
        contents = await file.read()

        # Check file size (50 MB limit)
        if len(contents) > 52_428_800:
            raise HTTPException(
                status_code=400,
                detail="Image is too large. Max size is 50 MB."
            )

        with open(tmp_path, "wb") as f:
            f.write(contents)

        # 3. Identify the plant with PlantNet
        try:
            scientific_name = identify_plant(tmp_path)
        except FileNotFoundError:
            raise HTTPException(status_code=500, detail="Temp file not found — this is a server error.")
        except ValueError as e:
            # Covers "not a plant" and other validation errors
            raise HTTPException(status_code=422, detail=str(e))
        except http_requests.exceptions.Timeout:
            raise HTTPException(status_code=504, detail="PlantNet took too long to respond. Please try again.")
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"PlantNet could not identify the plant. Try a clearer photo. ({e})"
            )

        # 4. Generate the Pokédex entry with Gemini
        try:
            result = generate_pokedex_entry(scientific_name)
        except ValueError as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=502,
                detail=f"Gemini could not generate an entry. ({e})"
            )

        # 5. Return everything to the frontend
        return {
            "scientific_name": result["scientific_name"],
            "entry": result["entry"],
            "model": result["model"],
        }

    finally:
        # Always clean up the temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)