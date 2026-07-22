from pydantic import BaseModel

class ProgramaBase(BaseModel):
    clave: str
    nombre: str
    descripcion: str | None = None

class ProgramaCreate(ProgramaBase):
    pass

class ProgramaUpdate(BaseModel):
    clave: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None

class ProgramaResponse(ProgramaBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True