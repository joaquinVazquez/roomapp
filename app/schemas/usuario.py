from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# =========================
# BASE
# =========================

class UsuarioBase(BaseModel):
    email: EmailStr
    rol_id: int


# =========================
# CREAR USUARIO
# =========================

class UsuarioCreate(UsuarioBase):
    nombre: str
    apellido: str
    password: str


# =========================
# LOGIN (opcional si usas OAuth2)
# =========================

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


# =========================
# RESPONSE
# =========================

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    created_at: Optional[datetime]

    class Config:
        from_attributes = True