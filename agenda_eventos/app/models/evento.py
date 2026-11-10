from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Evento(Base):

    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(primary_key=True)

    titulo: Mapped[str] = mapped_column(
        String(120),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    capacidad: Mapped[int] = mapped_column(
        nullable=False
    )