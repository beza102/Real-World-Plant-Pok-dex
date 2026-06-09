"""
Service module for interacting with the Groq Cloud API (Llama 3.1).
Handles generating Pokédex-style descriptions from a plant's scientific name.
"""
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.1-8b-instant"
MAX_TOKENS = 300