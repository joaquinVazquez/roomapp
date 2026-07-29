from sqlalchemy.orm import Session

from app.models.notificacion import Notificacion


def crear_notificacion(
    db: Session,
    usuario_id: int,
    mensaje: str,
    tipo_evento: str,
    referencia_id: int | None = None
):

    notificacion = Notificacion(
        usuario_id=usuario_id,
        mensaje=mensaje,
        tipo_evento=tipo_evento,
        referencia_id=referencia_id,
        leido=False
    )

    db.add(notificacion)

    db.commit()

    db.refresh(notificacion)

    return notificacion