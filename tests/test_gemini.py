from google import genai
from src.config import get_settings

settings = get_settings()

client = genai.Client(api_key=settings.google_api_key)

response = client.models.generate_content(
    model=settings.gemini_model,
    contents="Say hello"
)

print(response.text)