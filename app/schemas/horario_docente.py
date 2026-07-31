from pydantic import BaseModel
from typing import List


class ClaseDocente(BaseModel):

    hora: str
    materia: str
    grupo: str
    aula: str


class DiaDocente(BaseModel):

    dia: str
    clases: List[ClaseDocente]


class HorarioDocenteResponse(BaseModel):

    horarios: List[DiaDocente]