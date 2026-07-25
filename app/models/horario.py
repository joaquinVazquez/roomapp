from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Time
)

from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Horario(Base):

    __tablename__ = "horarios"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    actividad_academica_id = Column(
        Integer,
        ForeignKey("actividades_academicas.id"),
        nullable=False
    )

    dia_semana_id = Column(
    Integer,
    ForeignKey("dias_semana.id"),
    nullable=False
    )

    hora_inicio = Column(
        Time,
        nullable=False
    )

    hora_fin = Column(
        Time,
        nullable=False
    )

    aula_id = Column(
        Integer,
        ForeignKey("aulas.id"),
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

    # relaciones

    actividad_academica = relationship(
        "ActividadAcademica",
        back_populates="horarios"
    )

    aula = relationship(
        "Aula",
        back_populates="horarios"
    )

    dia_semana = relationship(
    "DiaSemana",
    back_populates="horarios"
    )