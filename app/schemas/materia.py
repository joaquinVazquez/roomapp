from pydantic import BaseModel

class MateriaBase(BaseModel):

    clave: str
    nombre: str
    descripcion: str | None = None


class MateriaCreate(MateriaBase):
    pass


class MateriaUpdate(BaseModel):

    clave: str | None = None
    nombre: str | None = None
    descripcion: str | None = None
    activo: bool | None = None


class MateriaResponse(MateriaBase):

    id: int
    activo: bool

    class Config:
        from_attributes = True