from fastapi import FastAPI
from pydantic import BaseModel

from app.gemini_service import generar_respuesta

app = FastAPI(
    title="DevTutor AI",
    description="Asistente educativo de programación con Inteligencia Artificial",
    version="1.0.0"
)

class PreguntaRequest(BaseModel):
    pregunta: str

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a DevTutor AI",
        "estado": "API funcionando correctamente"
    }

@app.post("/preguntar")
def preguntar(datos: PreguntaRequest):
    respuesta = generar_respuesta(datos.pregunta)

    return {
        "pregunta": datos.pregunta,
        "respuesta": respuesta
    }