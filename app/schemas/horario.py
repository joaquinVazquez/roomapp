from datetime import time, datetime
from typing import Optional

from pydantic import BaseModel


class HorarioBase(BaseModel):

    actividad_academica_id: int
    dia_semana_id: int

    hora_inicio: time
    hora_fin: time

    aula_id: Optional[int] = None


class HorarioCreate(HorarioBase):
    pass


class HorarioUpdate(BaseModel):

    actividad_academica_id: Optional[int] = None
    dia_semana_id: Optional[int] = None

    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None

    aula_id: Optional[int] = None


class HorarioResponse(HorarioBase):

    id: int
    created_at: datetime

    class Config:
        from_attributes = True