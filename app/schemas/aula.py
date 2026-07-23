from pydantic import BaseModel


class AulaBase(BaseModel):

    clave: str
    nombre: str
    capacidad: int
    tipo: str
    ubicacion: str | None = None
    descripcion: str | None = None


class AulaCreate(AulaBase):
    pass


class AulaUpdate(BaseModel):

    clave: str | None = None
    nombre: str | None = None
    capacidad: int | None = None
    tipo: str | None = None
    ubicacion: str | None = None
    descripcion: str | None = None
    activo: bool | None = None


class AulaResponse(AulaBase):

    id: int
    activo: bool

    class Config:
        from_attributes = True