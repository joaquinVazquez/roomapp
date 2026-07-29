from sqlalchemy.orm import Session

from app.models.notificacion import Notificacion



# =====================================
# CREAR NOTIFICACION
# =====================================

def crear_notificacion(
    db: Session,
    usuario_id: int,
    mensaje: str,
    tipo_evento: str = "GENERAL",
    referencia_id: int = None
):

    notificacion = Notificacion(

        usuario_id=usuario_id,

        mensaje=mensaje,

        tipo_evento=tipo_evento,

        referencia_id=referencia_id
    )


    db.add(notificacion)

    db.commit()

    db.refresh(notificacion)


    return notificacion




# =====================================
# OBTENER NO LEIDAS
# =====================================

def obtener_no_leidas(
    db: Session,
    usuario_id: int
):

    return (
        db.query(Notificacion)
        .filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leido == False
        )
        .order_by(
            Notificacion.created_at.desc()
        )
        .all()
    )




# =====================================
# MARCAR TODAS LEIDAS
# =====================================

def marcar_todas_leidas(
    db: Session,
    usuario_id: int
):

    notificaciones = (
        db.query(Notificacion)
        .filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leido == False
        )
        .all()
    )


    for n in notificaciones:

        n.leido = True


    db.commit()


    return len(notificaciones)




# =====================================
# CONTADOR
# =====================================

def contar_no_leidas(
    db: Session,
    usuario_id: int
):

    return (
        db.query(Notificacion)
        .filter(
            Notificacion.usuario_id == usuario_id,
            Notificacion.leido == False
        )
        .count()
    )