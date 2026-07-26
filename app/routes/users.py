from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.rol import Rol

from app.schemas.usuario import UsuarioCreate

from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)


# =========================
# CREAR USUARIO
# =========================

@router.post("/")
def create_user(
    user: UsuarioCreate,
    db: Session = Depends(get_db)
):

    # 🔹 Validar rol
    rol = db.query(Rol).filter(
        Rol.id == user.rol_id
    ).first()

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="El rol no existe"
        )

    # 🔹 Validar correo duplicado
    existe = db.query(Persona).filter(
        Persona.email == user.email
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )

    # 🔹 Crear persona
    persona = Persona(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email
    )

    db.add(persona)
    db.commit()
    db.refresh(persona)

    # 🔹 Crear usuario
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