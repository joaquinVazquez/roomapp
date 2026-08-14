from datetime import datetime

from sqlalchemy.orm import relationship

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
)

from app.db.base_class import Base


class PeriodoAcademico(Base):

    __tablename__ = "periodos_academicos"

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

    fecha_inicio = Column(
        Date,
        nullable=False
    )

    fecha_fin = Column(
        Date,
        nullable=False
    )

    # Indica si el periodo está habilitado dentro del sistema.
    # No significa necesariamente que esté actualmente en curso.
    activo = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    grupos = relationship(
        "Grupo",
        back_populates="periodo_academico"
    )

    inscripciones = relationship(
        "Inscripcion",
        back_populates="periodo_academico"
    )