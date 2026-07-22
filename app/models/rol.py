from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    descripcion = Column(String, nullable=True)

    activo = Column(Boolean, default=True)