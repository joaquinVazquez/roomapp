from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class RolPermiso(Base):

    __tablename__ = "rol_permisos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    rol_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False
    )

    permiso_id = Column(
        Integer,
        ForeignKey("permisos.id"),
        nullable=False
    )

    # =========================
    # RELACIONES
    # =========================

    rol = relationship(
        "Rol",
        back_populates="permisos"
    )

    permiso = relationship(
        "Permiso",
        back_populates="roles"
    )

    # =========================
    # RESTRICCIÓN
    # =========================

    __table_args__ = (
        UniqueConstraint(
            "rol_id",
            "permiso_id",
            name="uq_rol_permiso"
        ),
    )