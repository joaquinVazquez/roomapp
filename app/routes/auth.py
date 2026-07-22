from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.models.usuario import Usuario

from app.core.security import (
    verify_password,
    create_access_token,
    require_roles
)

router = APIRouter()


# ==========================
# LOGIN
# ==========================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = (
        db.query(Usuario)
        .filter(Usuario.email == form_data.username)
        .first()
    )

    if not db_user:
        return {
            "error": "Usuario no encontrado"
        }

    if not verify_password(
        form_data.password,
        db_user.password_hash
    ):
        return {
            "error": "Contraseña incorrecta"
        }

    access_token = create_access_token(
        data={
            "user_id": db_user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ==========================
# RUTA PROTEGIDA
# ==========================

@router.get("/admin-only")
def admin_only(
    current_user: Usuario = Depends(
        require_roles("ADMINISTRADOR")
    )
):
    return {
        "message": "Bienvenido administrador"
    }