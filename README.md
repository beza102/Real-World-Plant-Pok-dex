# Real-World Plant Pokedex

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
