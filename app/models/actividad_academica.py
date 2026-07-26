from datetime import datetime
from sqlalchemy import UniqueConstraint

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)

from sqlalchemy.orm import relationship
from app.db.base_class import Base

class ActividadAcademica(Base):

    __tablename__ = "actividades_academicas"

    __table_args__ = (
    UniqueConstraint(
        "grupo_id",
        "materia_id",
        "bloque",
        name="uq_grupo_materia_bloque"
    ),
)

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    grupo_id = Column(
        Integer,
        ForeignKey("grupos.id"),
        nullable=False
    )

    materia_id = Column(
        Integer,
        ForeignKey("materias.id"),
        nullable=False
    )

    docente_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    bloque = Column(
        String(20),
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

    grupo = relationship(
        "Grupo",
        back_populates="actividades_academicas"
    )

    materia = relationship(
        "Materia",
        back_populates="actividades_academicas"
    )

    docente = relationship(
        "Usuario",
        back_populates="actividades_academicas"
    )

    horarios = relationship(
    "Horario",
    back_populates="actividad_academica"
    )
    