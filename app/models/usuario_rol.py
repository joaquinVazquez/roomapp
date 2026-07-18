from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, UniqueConstraint
from datetime import datetime
from sqlalchemy.orm import relationship

from app.db.base import Base


class UsuarioRol(Base):
    __tablename__ = "usuario_roles"

    __table_args__ = (
        UniqueConstraint("usuario_id", "rol_id", name="uq_usuario_rol"),
    )

    id = Column(Integer, primary_key=True, index=True)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    fecha_asignacion = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)

    usuario = relationship("Usuario", backref="roles")
    rol = relationship("Rol")