from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GrupoBase(BaseModel):
    clave: str
    nombre: str
    turno: str
    programa_id: int
    periodo_academico_id: int
    activo: Optional[bool] = True


class GrupoCreate(GrupoBase):
    pass


class GrupoUpdate(BaseModel):
    clave: Optional[str] = None
    nombre: Optional[str] = None
    turno: Optional[str] = None
    programa_id: Optional[int] = None
    periodo_academico_id: Optional[int] = None
    activo: Optional[bool] = None


class GrupoResponse(GrupoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True