from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.evento_schema import EventoCreate, EventoResponse
from app.services.evento_service import EventoService


router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"]
)

service = EventoService()


def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[EventoResponse])
def get_eventos(db: Session = Depends(get_db)):

    return service.get_all(db)


@router.get("/{evento_id}", response_model=EventoResponse)
def get_evento(
    evento_id: int,
    db: Session = Depends(get_db)
):

    evento = service.get_by_id(db, evento_id)

    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado"
        )

    return evento


@router.post(
    "/",
    response_model=EventoResponse,
    status_code=status.HTTP_201_CREATED
)
def create_evento(
    datos: EventoCreate,
    db: Session = Depends(get_db)
):

    try:
        return service.create(db, datos)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )