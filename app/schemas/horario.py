from datetime import time, datetime
from pydantic import BaseModel


class HorarioBase(BaseModel):

    actividad_academica_id: int
    dia_semana_id: int
    hora_inicio: time
    hora_fin: time
    aula_id: int | None = None


class HorarioCreate(HorarioBase):
    """
    Datos necesarios para crear un horario.
    """
    pass


class HorarioUpdate(BaseModel):

    actividad_academica_id: int | None = None
    dia_semana_id: int | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    aula_id: int | None = None


class HorarioResponse(HorarioBase):

    id: int
    created_at: datetime

    class Config:
        from_attributes = True