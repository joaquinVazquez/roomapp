from passlib.context import CryptContext
from jose import JWTError, jwt

from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.usuario import Usuario
from app.models.rol import Rol


# ==================================================
# CONFIGURACIÓN JWT
# ==================================================

SECRET_KEY = "tu_clave_secreta_super_segura"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60



# ==================================================
# PASSWORD
# ==================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



def hash_password(password: str):

    return pwd_context.hash(password)



def verify_password(
    password_plano: str,
    password_hash: str
):

    return pwd_context.verify(
        password_plano,
        password_hash
    )



# ==================================================
# OAUTH2 SWAGGER
# ==================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)



# ==================================================
# CREAR TOKEN JWT
# ==================================================

def create_access_token(
    data: dict
):

    datos = data.copy()


    expiracion = (
        datetime.utcnow()
        +
        timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )


    datos.update(
        {
            "exp": expiracion
        }
    )


    token = jwt.encode(
        datos,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return token



# ==================================================
# OBTENER USUARIO DESDE TOKEN
# ==================================================

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )


        user_id = payload.get(
            "user_id"
        )


        if user_id is None:

            raise HTTPException(
                status_code=401,
                detail="Token inválido"
            )


    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )



    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.id == user_id
        )
        .first()
    )


    if usuario is None:

        raise HTTPException(
            status_code=401,
            detail="Usuario no encontrado"
        )


    return usuario



# ==================================================
# VALIDACIÓN POR ROLES
# ==================================================

def require_roles(*roles_permitidos):

    def role_checker(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        rol_usuario = (
            db.query(Rol)
            .filter(Rol.id == current_user.rol_id)
            .first()
        )

        if not rol_usuario:
            raise HTTPException(403, "Usuario sin rol")

        if rol_usuario.nombre not in roles_permitidos:
            raise HTTPException(403, "Sin permisos")

        return current_user

    return role_checker