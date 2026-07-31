from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db
from app.models.usuario import Usuario

from app.core.security import verify_password, create_access_token

router = APIRouter(tags=["Auth"])


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = (
        db.query(Usuario)
        .filter(Usuario.email == form_data.username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_access_token({
    "user_id": user.id,
    "rol": user.rol.nombre
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }