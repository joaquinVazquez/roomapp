from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.db.session import get_db

from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.rol import Rol

from app.schemas.user import UserCreate

from app.core.security import hash_password


router = APIRouter()


@router.post("/users")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    rol = (
        db.query(Rol)
        .filter(Rol.id == user.rol_id)
        .first()
    )


    if not rol:
        return {
            "error": "El rol no existe"
        }


    existe = (
        db.query(Persona)
        .filter(Persona.email == user.email)
        .first()
    )


    if existe:
        return {
            "error": "El correo ya existe"
        }


    persona = Persona(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email
    )


    db.add(persona)
    db.commit()
    db.refresh(persona)


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