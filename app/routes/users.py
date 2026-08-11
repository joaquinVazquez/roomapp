from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.rol import Rol

from app.schemas.usuario import UsuarioCreate

from app.core.security import hash_password
from app.core.security import get_current_user

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

# =========================
# LISTAR USUARIOS
# =========================

@router.get("/")
def get_users(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    # Solo administrador
    if current_user.rol.nombre != "ADMINISTRADOR":

        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para consultar usuarios"
        )


    usuarios = (
        db.query(Usuario)
        .join(Persona)
        .join(Rol)
        .all()
    )


    resultado = []


    for usuario in usuarios:

        resultado.append({

            "id": usuario.id,

            "nombre": usuario.persona.nombre,

            "apellido": usuario.persona.apellido,

            "email": usuario.email,

            "rol": usuario.rol.nombre,

            "activo": usuario.activo

        })


    return resultado

# =========================
# USUARIO ACTUAL
# =========================

@router.get("/me")
def get_me(
    current_user: Usuario = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "rol": current_user.rol.nombre
    }

@router.get("/debug-user")
def debug_user(
    current_user: Usuario = Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "email": current_user.email,
        "rol_id": current_user.rol_id,
        "rol": current_user.rol.nombre
    }

# =========================
# ACTIVAR / DESACTIVAR USUARIO
# =========================

@router.patch("/{user_id}/toggle")
def toggle_usuario(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    # 🔒 Solo admin
    if current_user.rol.nombre != "ADMINISTRADOR":
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos"
        )

    usuario = db.query(Usuario).filter(
        Usuario.id == user_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    # 🔁 cambiar estado
    usuario.activo = not usuario.activo

    db.commit()
    db.refresh(usuario)

    return {
        "message": "Estado actualizado",
        "usuario_id": usuario.id,
        "activo": usuario.activo
    }