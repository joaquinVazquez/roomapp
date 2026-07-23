from datetime import datetime

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


class Grupo(Base):

    __tablename__ = "grupos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    clave = Column(
        String(30),
        unique=True,
        nullable=False,
        index=True
    )

    nombre = Column(
        String(100),
        nullable=False
    )

    turno = Column(
        String(30),
        nullable=False
    )

    programa_id = Column(
        Integer,
        ForeignKey("programas.id"),
        nullable=False
    )

    periodo_academico_id = Column(
        Integer,
        ForeignKey("periodos_academicos.id"),
        nullable=False
    )

    programa = relationship(
    "Programa",
    back_populates="grupos"
    )

    periodo_academico = relationship(
        "PeriodoAcademico",
        back_populates="grupos"
    )

    actividades_academicas = relationship(
    "ActividadAcademica",
    back_populates="grupo"
    )

    activo = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )