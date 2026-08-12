from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Rol(Base):

    __tablename__ = "roles"

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

    # =========================
    # RELACIÓN CON PERMISOS
    # =========================

    permisos = relationship(
        "RolPermiso",
        back_populates="rol",
        cascade="all, delete-orphan"
    )