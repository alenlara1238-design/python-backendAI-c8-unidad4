from google.genai import types

from app.gemini_client import client
from app.prompts.support_prompts import SUPPORT_SYSTEM_PROMPT

def responder_consulta(pregunta: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= pregunta,
        config=types.GenerateContentConfig(system_instruction=SUPPORT_SYSTEM_PROMPT)

    )
    return response.text