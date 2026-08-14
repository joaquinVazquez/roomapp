from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ActividadAcademicaBase(BaseModel):
    grupo_id: int
    materia_id: int
    docente_id: int
    periodo_academico_id: int
    bloque: Optional[str] = None
    activo: Optional[bool] = True


class ActividadAcademicaCreate(ActividadAcademicaBase):
    pass


class ActividadAcademicaUpdate(BaseModel):
    grupo_id: Optional[int] = None
    materia_id: Optional[int] = None
    docente_id: Optional[int] = None
    periodo_academico_id: Optional[int] = None
    bloque: Optional[str] = None
    activo: Optional[bool] = None


class ActividadAcademicaResponse(ActividadAcademicaBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        from_attributes = True