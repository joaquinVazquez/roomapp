from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class RolPermiso(Base):

    __tablename__ = "roles_permisos"

    id = Column(Integer, primary_key=True)

    rol_id = Column(Integer, ForeignKey("roles.id"))
    permiso_id = Column(Integer, ForeignKey("permisos.id"))

    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")