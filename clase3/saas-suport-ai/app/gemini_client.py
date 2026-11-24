from google import genai
from app.config import GEMINI_API_KEY

#Este es el cliente de Gemini
client = genai.Client(api_key=GEMINI_API_KEY)