from app.db.session import SessionLocal
from app.models.notificacion import Notificacion


def run():

    db = SessionLocal()

    print("\n--- TEST MARCAR NOTIFICACION LEIDA ---\n")

    try:

        # ==================================
        # 1. BUSCAR NOTIFICACION
        # ==================================

        notificacion_id = 8   # cambia si es necesario

        notificacion = db.query(Notificacion).filter(
            Notificacion.id == notificacion_id
        ).first()


        if notificacion is None:
            print("❌ Notificación no encontrada")
            return


        print("Antes:")
        print("----------------")
        print("ID:", notificacion.id)
        print("Usuario:", notificacion.usuario_id)
        print("Mensaje:", notificacion.mensaje)
        print("Leído:", notificacion.leido)


        # ==================================
        # 2. MARCAR COMO LEIDA
        # ==================================

        notificacion.leido = True

        db.commit()
        db.refresh(notificacion)


        print("\nDespués:")
        print("----------------")
        print("ID:", notificacion.id)
        print("Usuario:", notificacion.usuario_id)
        print("Mensaje:", notificacion.mensaje)
        print("Leído:", notificacion.leido)


        print("\n✔ Test completado")


    except Exception as e:

        print("❌ Error:", e)

    finally:

        db.close()



if __name__ == "__main__":
    run()