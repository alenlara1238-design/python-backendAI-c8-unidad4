from sqlalchemy.orm import Session

from app.models.evento import Evento
from app.schemas.evento_schema import EventoCreate
from app.repositories.evento_repository import EventoRepository


class EventoService:

    def __init__(self):
        self.repository = EventoRepository()

    def get_all(self, db: Session) -> list[Evento]:

        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        evento_id: int
    ) -> Evento | None:

        return self.repository.get_by_id(db, evento_id)

    def create(
        self,
        db: Session,
        datos: EventoCreate
    ) -> Evento:

        # Regla 1: el título no puede estar vacío.
        if not datos.titulo.strip():
            raise ValueError("El título del evento es obligatorio")

        # Regla 2: la capacidad debe ser mayor que cero.
        if datos.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")

        evento = Evento(
            titulo=datos.titulo.strip(),
            descripcion=datos.descripcion,
            capacidad=datos.capacidad
        )

        return self.repository.create(db, evento)

    def update(
        self,
        db: Session,
        evento_id: int,
        datos: EventoCreate
    ) -> Evento | None:

        evento = self.repository.get_by_id(db, evento_id)

        if evento is None:
            return None

        # Regla 1: el título no puede estar vacío.
        if not datos.titulo.strip():
            raise ValueError("El título del evento es obligatorio")

        # Regla 2: la capacidad debe ser mayor que cero.
        if datos.capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero")

        evento.titulo = datos.titulo.strip()
        evento.descripcion = datos.descripcion
        evento.capacidad = datos.capacidad

        return self.repository.update(db, evento)