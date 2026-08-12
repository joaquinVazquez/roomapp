from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import get_current_user

from app.models.usuario import Usuario
from app.models.permiso import Permiso
from app.models.rol_permiso import RolPermiso


def require_permiso(nombre_permiso: str):

    def verificar_permiso(
        db: Session = Depends(get_db),
        current_user: Usuario = Depends(get_current_user)
    ):

        permisos = (
            db.query(Permiso.nombre)
            .join(
                RolPermiso,
                Permiso.id == RolPermiso.permiso_id
            )
            .filter(
                RolPermiso.rol_id == current_user.rol_id
            )
            .all()
        )

        permisos_usuario = [
            permiso[0]
            for permiso in permisos
        ]

        if nombre_permiso not in permisos_usuario:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para realizar esta acción"
            )

        return current_user

    return verificar_permiso