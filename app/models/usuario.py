from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)

    persona_id = Column(
        Integer,
        ForeignKey("personas.id"),
        nullable=False
    )

    rol_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = Column(
        String,
        nullable=False
    )

    activo = Column(
        Boolean,
        default=True
    )

    ultimo_acceso = Column(
        DateTime,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    # relaciones

    persona = relationship(
        "Persona",
        back_populates="usuario"
    )

    rol = relationship(
        "Rol"
    )

    actividades_academicas = relationship(
    "ActividadAcademica",
    back_populates="docente"
    )