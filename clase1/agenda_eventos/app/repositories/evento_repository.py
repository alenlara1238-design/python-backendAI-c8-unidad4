from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.evento import Evento


class EventoRepository:

    def get_all(self, db: Session) -> list[Evento]:

        statement = select(Evento)

        return list(db.scalars(statement).all())

    def get_by_id(
        self,
        db: Session,
        evento_id: int
    ) -> Evento | None:

        return db.get(Evento, evento_id)

    def create(
        self,
        db: Session,
        evento: Evento
    ) -> Evento:

        try:
            db.add(evento)
            db.commit()
            db.refresh(evento)

            return evento

        except Exception:
            db.rollback()
            raise

    def update(
        self,
        db: Session,
        evento: Evento
    ) -> Evento:

        try:
            db.commit()
            db.refresh(evento)

            return evento

        except Exception:
            db.rollback()
            raise