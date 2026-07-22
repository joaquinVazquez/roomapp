from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.db.session import get_db

from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.rol import Rol

from app.schemas.user import UserCreate

from app.core.security import (
    verify_password,
    create_access_token,
    require_roles,
    hash_password
)


router = APIRouter()


# ==============================
# CREAR USUARIO
# ==============================

@router.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    # validar rol

    rol = db.query(Rol).filter(
        Rol.id == user.rol_id
    ).first()

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="El rol no existe"
        )


    # validar correo

    existe = db.query(Persona).filter(
        Persona.email == user.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )


    # crear persona

    persona = Persona(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email
    )

    db.add(persona)
    db.commit()
    db.refresh(persona)


    # crear usuario

    usuario = Usuario(
        persona_id=persona.id,
        rol_id=user.rol_id,
        email=user.email,
        password_hash=hash_password(user.password),
        activo=True
    )


    db.add(usuario)
    db.commit()
    db.refresh(usuario)


    return {
        "message": "Usuario creado correctamente",
        "usuario_id": usuario.id
    }



# ==============================
# LOGIN
# ==============================

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.email == form_data.username
    ).first()


    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )


    if not verify_password(
        form_data.password,
        usuario.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Contraseña incorrecta"
        )


    token = create_access_token(
        {
            "user_id": usuario.id
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer"
    }



# ==============================
# PRUEBA DE PERMISOS
# ==============================

@router.get("/admin-only")
def admin_only(
    user = Depends(
        require_roles("ADMINISTRADOR")
    )
):

    return {
        "message": "Bienvenido administrador"
    }