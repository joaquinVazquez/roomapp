from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.notificacion import Notificacion
from app.core.deps import get_current_user

router = APIRouter(prefix="/notificaciones", tags=["Notificaciones"])


@router.get("/")
def mis_notificaciones(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db.query(Notificacion).filter(
        Notificacion.usuario_id == current_user.id
    ).all()