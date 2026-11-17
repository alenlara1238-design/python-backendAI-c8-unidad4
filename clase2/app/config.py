import os
from dotenv import load_dotenv

#cargar las variables del archivo .env
load_dotenv()

#Obtener la API Key de gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")