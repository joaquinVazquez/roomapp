from datetime import datetime
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)

from app.db.base_class import Base


class Aula(Base):

    __tablename__ = "aulas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    clave = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    capacidad = Column(
        Integer,
        nullable=False
    )

    tipo = Column(
        String(50),
        nullable=False
    )

    ubicacion = Column(
        String(100),
        nullable=True
    )

    descripcion = Column(
        String(255),
        nullable=True
    )

    activo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    horarios = relationship(
    "Horario",
    back_populates="aula"
)