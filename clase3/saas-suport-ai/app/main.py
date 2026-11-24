from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.prompts.prompt_library import PROMPT_TEMPLATES

from app.services.chatbot_service import responder_consulta
from app.services.promtp_service import generar_prompt

app = FastAPI(
    title= "SaaS Support AI",
    description = "Asistente inteligente para soporte de Nexus",
    version="1.0.0"
)

#Modelo para recibir la pregunta
class PreguntaRequest(BaseModel):
    pregunta: str = Field(
        min_length=3,
        max_length=1000,
        description ="Consulta relacionada con Nexus SaaS"
    )

class PromptRequest(BaseModel):
    nombre: str
    datos: dict

@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Saas Support AI"
    }

@app.post("/soporte/preguntar")
def preguntar_soporte(datos: PreguntaRequest):
    try:
        respuesta = responder_consulta(datos.pregunta)

        return {
            "pregunta": datos.pregunta,
            "respuesta": respuesta
        }
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al consultar el servicio de IA: {str(error)}"
        )

@app.get("/prompts")
def listar_prompts():
    return {
        "total": len(PROMPT_TEMPLATES),
        "plantillas": list(PROMPT_TEMPLATES.keys())
    }

@app.post("/prompts/generar")
def crear_prompt(datos: PromptRequest):
    try:
        prompt = generar_prompt(
            datos.nombre,
            datos.datos
        )
        return {
            "plantilla": datos.nombre,
            "prompt_generado": prompt
        }
    
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

