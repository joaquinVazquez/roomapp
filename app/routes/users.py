from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.usuario import Usuario
from app.models.persona import Persona
from app.models.rol import Rol

from app.schemas.usuario import UsuarioCreate

from app.core.security import hash_password
from app.core.security import get_current_user

from app.core.permissions import require_permiso


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)


# =========================================================
# CREAR USUARIO
# =========================================================

@router.post(
    "/",
    dependencies=[
        Depends(require_permiso("GESTIONAR_USUARIOS"))
    ]
)
def create_user(
    user: UsuarioCreate,
    db: Session = Depends(get_db)
):

    # =====================================================
    # VALIDAR ROL
    # =====================================================

    rol = (
        db.query(Rol)
        .filter(
            Rol.id == user.rol_id
        )
        .first()
    )

    if not rol:

        raise HTTPException(
            status_code=404,
            detail="El rol no existe"
        )


    # =====================================================
    # VALIDAR CORREO DUPLICADO
    # =====================================================

    existe = (
        db.query(Persona)
        .filter(
            Persona.email == user.email
        )
        .first()
    )

    if existe:

        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )


    # =====================================================
    # CREAR PERSONA
    # =====================================================

    persona = Persona(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email
    )

    db.add(persona)

    db.commit()

    db.refresh(persona)


    # =====================================================
    # CREAR USUARIO
    # =====================================================

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


    # =====================================================
    # RESPUESTA
    # =====================================================

    return {
        "message": "Usuario creado correctamente",
        "usuario_id": usuario.id
    }


# =========================================================
# LISTAR USUARIOS
# =========================================================

@router.get(
    "/",
    dependencies=[
        Depends(require_permiso("GESTIONAR_USUARIOS"))
    ]
)
def get_users(
    db: Session = Depends(get_db)
):

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


# =========================================================
# USUARIO ACTUAL
# =========================================================

@router.get("/me")
def get_me(
    current_user: Usuario = Depends(get_current_user)
):

    return {

        "id": current_user.id,

        "email": current_user.email,

        "rol": current_user.rol.nombre

    }


# =========================================================
# DEBUG USUARIO ACTUAL
# =========================================================

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


# =========================================================
# ACTIVAR / DESACTIVAR USUARIO
# =========================================================

@router.patch(
    "/{user_id}/toggle",
    dependencies=[
        Depends(require_permiso("GESTIONAR_USUARIOS"))
    ]
)
def toggle_usuario(
    user_id: int,
    db: Session = Depends(get_db)
):

    # =====================================================
    # BUSCAR USUARIO
    # =====================================================

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.id == user_id
        )
        .first()
    )


    if not usuario:

        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )


    # =====================================================
    # CAMBIAR ESTADO
    # =====================================================

    usuario.activo = not usuario.activo

    db.commit()

    db.refresh(usuario)


    # =====================================================
    # RESPUESTA
    # =====================================================

    return {

        "message": "Estado actualizado",

        "usuario_id": usuario.id,

        "activo": usuario.activo

    }