"""
Service module for interacting with the Google Gemini API.
Handles generating Pokédex-style descriptions from a plant's scientific name.
"""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
MAX_TOKENS = 300

SYSTEM_PROMPT = """You are a Pokédex — a field guide that describes real-world plants
in the style of a Pokémon entry. Your tone is enthusiastic, slightly dramatic, and
educational. Every entry must include exactly three things:
1. Habitat: where this plant naturally grows (one sentence)
2. Cool Fact: one surprising or delightful fact about this plant (one sentence)
3. Care Difficulty: rate it as Easy, Moderate, or Challenging, with a one-sentence reason.

Keep the total response under 80 words. Do not use bullet points or headers —
write it as flowing prose, like a real Pokédex screen. Do not make up species that
don't exist. If you are unsure about a detail, say so briefly rather than inventing facts."""


def generate_pokedex_entry(scientific_name: str) -> dict:
    """
    Generate a Pokédex-style description for a plant species.

    Args:
        scientific_name (str): The scientific name of the plant
                               (e.g. 'Taraxacum officinale'), typically
                               returned by identify_plant() in plantnet.py.
    Returns:
        dict with keys:
            - scientific_name (str): echoed back from input
            - entry (str): the Pokédex description text
            - model (str): which model generated it
    Raises:
        ValueError: if scientific_name is empty or GEMINI_API_KEY is not set
        google.genai.errors.APIError: for Gemini API-level errors
    """
    if not isinstance(scientific_name, str) or not scientific_name.strip():
        raise ValueError("scientific_name must be a non-empty string.")

    scientific_name = scientific_name.strip()

    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. Add it to backend/.env and save the file."
        )

    user_prompt = (
        f"Write a Pokédex entry for the real plant species: {scientific_name}. "
        "Include its habitat, one cool fact, and its care difficulty."
    )

    client = genai.Client(api_key=GEMINI_API_KEY)

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.75,
                max_output_tokens=MAX_TOKENS,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        entry_text = response.text.strip()
        return {
            "scientific_name": scientific_name,
            "entry": entry_text,
            "model": GEMINI_MODEL,
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        raise


if __name__ == "__main__":
    test_name = "Taraxacum officinale"  # common dandelion
    result = generate_pokedex_entry(test_name)
    print(f"Plant:  {result['scientific_name']}")
    print(f"Model:  {result['model']}")
    print(f"\n{result['entry']}")
