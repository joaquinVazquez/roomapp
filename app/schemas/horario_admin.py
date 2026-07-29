from pydantic import BaseModel
from typing import Optional


class HorarioAdminDTO(BaseModel):
    id: int
    dia: str
    hora_inicio: str
    hora_fin: str
    aula: Optional[str]
    materia: str
    grupo: str
    docente: str

    class Config:
        from_attributes = True