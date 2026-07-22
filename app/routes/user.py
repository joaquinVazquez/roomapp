from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserLogin
from app.models.usuario import Usuario
from app.db.session import get_db
from app.core.security import verify_password, create_access_token, require_roles
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


# 🔹 ENDPOINT 1 — CREAR USUARIO
# @router.post("/users")
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
#     new_user = User(
#         nombre=user.nombre,
#         email=user.email,
#         password=hash_password(user.password),
#         rol_id=user.rol_id
#     )

#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "Usuario creado correctamente"}


# 🔹 ENDPOINT 2 — LOGIN 
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    db_user = db.query(Usuario).filter(Usuario.email == form_data.username).first()

    if not db_user:
        return {"error": "Usuario no encontrado"}

    if not verify_password(form_data.password, db_user.password_hash):
        return {"error": "Contraseña incorrecta"}

    access_token = create_access_token(
        data={
            "user_id": db_user.id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/admin-only")
def admin_only(user = Depends(require_roles("ADMINISTRADOR"))):
    return {"message": "Bienvenido administrador"}