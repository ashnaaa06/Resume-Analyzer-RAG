# scripts/list_models.py

from google import genai
from src.config import get_settings

settings = get_settings()

client = genai.Client(api_key=settings.google_api_key)

for model in client.models.list():
    print(model.name)