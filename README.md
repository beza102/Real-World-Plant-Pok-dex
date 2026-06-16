# Real-World Plant Pokedex

A web app where you take a photo of any plant and get a real Pokédex-style entry, complete with habitat, a cool fact, care difficulty, and a voice that reads it aloud.

## How It Works

1. Upload or take a photo of a plant
2. PlantNet AI identifies the species
3. Gemini AI writes a Pokédex-style description
4. The app displays the entry and reads it out loud

## Quick Start

Create `backend/.env` with both API keys:

PLANTNET_API_KEY=your_plantnet_key_here
GEMINI_API_KEY=your_gemini_key_here

Start the backend from `backend/`:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Start the frontend in a new terminal from `frontend/`:

```bash
npm install
npm run dev
```
Then open [http://localhost:5173](http://localhost:5173) in your browser.

---

## The Eye — Plant Identification
**Service** · `backend/services/plantnet.py`

Uses the **PlantNet API** to identify a plant species from a photo.

Get a free key at [my.plantnet.org](https://my.plantnet.org) (free up to 500 IDs/day)

### Test
```bash
python -m pytest test/test_plantnet.py -v
```

---

## The Brain

The Brain uses **Google Gemini** (`gemini-2.5-flash`) to turn a plant's scientific name into a short, fun Pokédex-style entry — habitat, a cool fact, and care difficulty.

**Service:** `backend/services/gemini_service.py`

### Setup

Create `backend/.env` with:

```
GEMINI_API_KEY=your_key_here
```

Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

Install dependencies from the `backend/` directory:

```bash
python -m pip install -r requirements.txt
```

### Run

From `backend/`:

```bash
python services/gemini_service.py
```

Or use it in code after PlantNet identifies a plant:

```python
from services.gemini_service import generate_pokedex_entry

result = generate_pokedex_entry("Taraxacum officinale")
print(result["entry"])
```

### Test

```bash
python -m pytest test/test_gemini.py test/test_pipeline.py -v
```

## The Voice — Frontend & UI
**Service** · `frontend/src/`

Built with **React**. Handles the photo upload, displays the Pokédex card, and reads the entry aloud using the Web Speech API built into every browser.

Components:
- `ImageUpload.jsx` — drag and drop or camera upload
- `PokedexCard.jsx` — displays the plant name and entry
- `VoicePlayer.jsx` — reads the entry out loud

---

## The Backbone — Backend & API Pipeline
**Service** · `backend/main.py`

Built with **FastAPI**. Connects the frontend to PlantNet and Gemini, handles file uploads, and returns the final result. Also handles errors — if a non-plant photo is uploaded, the app shows a friendly message instead of crashing.

### Endpoints
- `GET /` — health check
- `POST /identify` — accepts an image, returns the plant name and Pokédex entry

---
