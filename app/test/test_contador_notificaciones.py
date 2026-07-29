from app.db.session import SessionLocal
from app.models.notificacion import Notificacion


def run():

    db = SessionLocal()

    print("\n--- TEST CONTADOR NOTIFICACIONES ---\n")


    usuario_id = 2


    total = db.query(Notificacion).filter(
        Notificacion.usuario_id == usuario_id,
        Notificacion.leido == False
    ).count()


    print(
        f"Usuario {usuario_id} tiene {total} notificaciones pendientes"
    )


    print("\n✔ Test completado")


    db.close()



if __name__ == "__main__":
    run()