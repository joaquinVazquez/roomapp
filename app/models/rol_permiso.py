from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class RolPermiso(Base):

    __tablename__ = "rol_permisos"

    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id"), nullable=False)

    # relaciones
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")