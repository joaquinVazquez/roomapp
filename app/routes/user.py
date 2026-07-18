from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.db.session import get_db
from app.core.security import hash_password, verify_password
from app.core.security import create_access_token
from app.core.security import require_roles

router = APIRouter()


# 🔹 ENDPOINT 1 — CREAR USUARIO
@router.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    new_user = User(
        nombre=user.nombre,
        email=user.email,
        password=hash_password(user.password),
        rol_id=user.rol_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario creado correctamente"}


# 🔹 ENDPOINT 2 — LOGIN 
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return {"error": "Usuario no encontrado"}

    if not verify_password(user.password, db_user.password):
        return {"error": "Contraseña incorrecta"}

    access_token = create_access_token(
    data={
        "user_id": db_user.id,
        "rol_id": db_user.rol_id
    }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/admin-only")
def admin_only(user = Depends(require_roles(1))):
    return {"message": "Bienvenido administrador"}