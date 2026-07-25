from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class DiaSemana(Base):

    __tablename__ = "dias_semana"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre = Column(
        String(20),
        nullable=False,
        unique=True
    )

    abreviatura = Column(
        String(5),
        nullable=False,
        unique=True
    )

    numero = Column(
        Integer,
        nullable=False,
        unique=True
    )

    activo = Column(
        Boolean,
        default=True
    )


    horarios = relationship(
        "Horario",
        back_populates="dia_semana"
    )