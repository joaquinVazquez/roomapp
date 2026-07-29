from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Boolean
)

from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Notificacion(Base):

    __tablename__ = "notificaciones"


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


    mensaje = Column(
        String,
        nullable=False
    )


    tipo_evento = Column(
        String(50),
        nullable=False,
        default="GENERAL"
    )


    referencia_id = Column(
        Integer,
        nullable=True
    )


    leido = Column(
        Boolean,
        default=False
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    usuario = relationship(
        "Usuario"
    )