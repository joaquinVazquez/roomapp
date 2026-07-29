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

@router.patch("/{notificacion_id}/leer")
def marcar_leida(
    notificacion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    notificacion = db.query(Notificacion).filter(
        Notificacion.id == notificacion_id,
        Notificacion.usuario_id == current_user.id
    ).first()


    if notificacion is None:
        raise HTTPException(
            status_code=404,
            detail="Notificación no encontrada"
        )


    notificacion.leido = True

    db.commit()
    db.refresh(notificacion)


    return {
        "mensaje": "Notificación marcada como leída",
        "id": notificacion.id,
        "leido": notificacion.leido
    }

@router.get("/no-leidas/count")
def contar_no_leidas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    total = db.query(Notificacion).filter(
        Notificacion.usuario_id == current_user.id,
        Notificacion.leido == False
    ).count()


    return {
        "total": total
    }