from pydantic import BaseModel
from typing import List


# =========================
# DTO CLASE INDIVIDUAL
# =========================
class ClaseEstudianteDTO(BaseModel):
    hora: str
    materia: str
    grupo: str
    aula: str
    docente: str


# =========================
# DTO POR DÍA
# =========================
class DiaHorarioDTO(BaseModel):
    dia: str
    clases: List[ClaseEstudianteDTO]


# =========================
# RESPONSE COMPLETO
# =========================
class HorarioEstudianteResponse(BaseModel):
    horarios: List[DiaHorarioDTO]