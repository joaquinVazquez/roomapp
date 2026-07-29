from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Inscripcion(Base):

    __tablename__ = "inscripciones"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id"),
        nullable=False
    )


    grupo_id = Column(
        Integer,
        ForeignKey("grupos.id"),
        nullable=False
    )


    periodo_academico_id = Column(
        Integer,
        ForeignKey("periodos_academicos.id"),
        nullable=False
    )


    activo = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    # Relaciones

    usuario = relationship(
        "Usuario",
        back_populates="inscripciones"
    )


    grupo = relationship(
        "Grupo",
        back_populates="inscripciones"
    )


    periodo_academico = relationship(
    "PeriodoAcademico",
    back_populates="inscripciones"
    )