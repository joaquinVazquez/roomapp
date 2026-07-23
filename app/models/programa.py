from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Programa(Base):
    __tablename__ = "programas"

    id = Column(Integer, primary_key=True, index=True)

    clave = Column(
        String(20),
        unique=True,
        nullable=False,
        index=True
    )

    nombre = Column(
        String(150),
        nullable=False
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

    materias = relationship(
    "ProgramaMateria",
    back_populates="programa"
    )

    grupos = relationship(
    "Grupo",
    back_populates="programa"
    )