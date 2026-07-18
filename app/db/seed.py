from sqlalchemy.orm import Session
from app.models.rol import Rol


def seed_roles(db: Session):
    roles = [
        "ADMINISTRADOR",
        "COORDINADOR_ACADEMICO",
        "DOCENTE",
        "ESTUDIANTE",
        "PERSONAL_ADMINISTRATIVO",
    ]

    for rol_nombre in roles:
        existe = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
        if not existe:
            nuevo_rol = Rol(nombre=rol_nombre)
            db.add(nuevo_rol)

    db.commit()