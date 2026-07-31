from pydantic import BaseModel
from typing import List


class ClaseEstudiante(BaseModel):
    hora: str
    materia: str
    grupo: str
    aula: str
    docente: str


class DiaHorario(BaseModel):
    dia: str
    clases: List[ClaseEstudiante]


class HorarioEstudianteResponse(BaseModel):
    dias: List[DiaHorario]