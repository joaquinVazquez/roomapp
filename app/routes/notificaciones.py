from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.notificacion import Notificacion
from app.models.usuario import Usuario
from app.core.security import get_current_user

router = APIRouter(
    prefix="/notificaciones",
    tags=["Notificaciones"]
)


# =========================
# MIS NOTIFICACIONES
# =========================
@router.get("/mis-notificaciones")
def mis_notificaciones(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    notificaciones = (
        db.query(Notificacion)
        .filter(
            Notificacion.usuario_id == current_user.id
        )
        .order_by(Notificacion.created_at.desc())
        .all()
    )

    resultado = []

    for n in notificaciones:
        resultado.append({
            "id": n.id,
            "mensaje": n.mensaje,
            "tipo": n.tipo_evento,
            "leido": n.leido,
            "fecha": n.created_at
        })

    return resultado