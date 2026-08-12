from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Permiso(Base):

    __tablename__ = "permisos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre = Column(
        String,
        unique=True,
        nullable=False
    )

    descripcion = Column(
        String,
        nullable=True
    )

    activo = Column(
        Boolean,
        default=True
    )

    # =========================
    # RELACIÓN CON ROLES
    # =========================

    roles = relationship(
        "RolPermiso",
        back_populates="permiso",
        cascade="all, delete-orphan"
    )