from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.gemini_service import (generar_respuesta, es_pregunta_de_programacion)

app = FastAPI(
    title="DevTutor AI",
    description="Asistente educativo de programación con Inteligencia Artificial",
    version="1.0.0"
)

class PreguntaRequest(BaseModel):
    pregunta: str = Field(
        min_length=3,
        max_length=500,
        description="Pregunta que el estudiante desea realizar"
    )

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a DevTutor AI",
        "estado": "API funcionando correctamente"
    }

@app.post("/preguntar")
def preguntar(datos: PreguntaRequest):

    try:
        # primero verificamos el dominio de la pregunta
        permitida = es_pregunta_de_programacion(datos.pregunta)

        # Si no pertenece al dominio de la pregunta:
        if not permitida:
            return {
                "pregunta: "datos.pregunta,
                "respuesta": (
                    "Soy DevTutor AI, un asistente especializado"
                    "en programación y desarrollo de software"
                    "no puedo ayudarte con consultas ajenas a este ámbito"
                ),
                "permitida": False
            }

        #Si está permitida, generamos la respuesta:
        respuesta = generar_respuesta(datos.pregunta)
        return {
                "pregunta": datos.pregunta,
                "respuesta": respuesta,
                "permitida": True
            }    
        
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar la IA: {str(error)}"
        )