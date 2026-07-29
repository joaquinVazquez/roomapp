from pydantic import BaseModel
from typing import List


class ClaseDocenteDTO(BaseModel):
    hora: str
    materia: str
    grupo: str
    aula: str


class DiaHorarioDocenteDTO(BaseModel):
    dia: str
    clases: List[ClaseDocenteDTO]


class HorarioDocenteResponse(BaseModel):
    horarios: List[DiaHorarioDocenteDTO]