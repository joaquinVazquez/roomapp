from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# BASE
# ============================================================

class InscripcionBase(BaseModel):

    usuario_id: int
    grupo_id: int
    periodo_academico_id: int
    activo: Optional[bool] = True


# ============================================================
# CREAR
# ============================================================

class InscripcionCreate(InscripcionBase):
    pass


# ============================================================
# ACTUALIZAR
# ============================================================

class InscripcionUpdate(BaseModel):

    grupo_id: Optional[int] = None
    periodo_academico_id: Optional[int] = None
    activo: Optional[bool] = None


# ============================================================
# RESPUESTA
# ============================================================

class InscripcionResponse(InscripcionBase):

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )