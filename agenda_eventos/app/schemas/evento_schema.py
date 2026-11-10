from pydantic import BaseModel, ConfigDict


class EventoCreate(BaseModel):
    titulo: str
    descripcion: str | None = None
    capacidad: int


class EventoResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    descripcion: str | None
    capacidad: int