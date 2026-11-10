import os

from fastapi import FastAPI

from app.database import Base, engine
from app.models import evento
from app.routers.evento_router import router as evento_router


# Crea las tablas que todavía no existen.
# Las pruebas fijan TESTING=1 para no abrir la base de desarrollo.
if os.getenv("TESTING") != "1":
    Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Agenda de Eventos API",
    description="API para administrar eventos",
    version="1.0.0"
)


app.include_router(evento_router)


@app.get("/")
def inicio():

    return {
        "mensaje": "Bienvenido a la API de Agenda de Eventos"
    }