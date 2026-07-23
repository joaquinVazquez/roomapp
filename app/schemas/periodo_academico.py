from datetime import date
from pydantic import BaseModel


class PeriodoAcademicoBase(BaseModel):

    clave: str
    nombre: str
    fecha_inicio: date
    fecha_fin: date


class PeriodoAcademicoCreate(PeriodoAcademicoBase):
    pass


class PeriodoAcademicoUpdate(BaseModel):

    clave: str | None = None
    nombre: str | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    activo: bool | None = None


class PeriodoAcademicoResponse(PeriodoAcademicoBase):

    id: int
    activo: bool

    class Config:
        from_attributes = True