from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.usuario import Usuario
from app.models.rol_permiso import RolPermiso
from app.models.permiso import Permiso

from app.core.security import get_current_user


def require_permission(nombre_permiso: str):

    def permiso_dependency(
        current_user: Usuario = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):

        permisos = (
            db.query(Permiso.nombre)
            .join(RolPermiso, Permiso.id == RolPermiso.permiso_id)
            .filter(RolPermiso.rol_id == current_user.rol_id)
            .all()
        )

        permisos_usuario = [p[0] for p in permisos]

        if nombre_permiso not in permisos_usuario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para esta acción"
            )

        return current_user

    return permiso_dependency