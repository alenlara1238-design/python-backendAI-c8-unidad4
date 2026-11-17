# Este componenteTiene como única responsabilidad comunicarse con Gemini

from google import genai
from app.config import GEMINI_API_KEY

#crear el cliente de Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# Seleccionar el modelo
MODEL_ID = "gemini-3.8-flash"

def generar_respuesta(pregunta: str)-> str:
    
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=pregunta
    )

    return response.text