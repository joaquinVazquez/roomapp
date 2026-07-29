from app.db.session import SessionLocal
from app.services.horario_service import reasignar_aula
from app.models.notificacion import Notificacion


def run():

    db = SessionLocal()


    print("\n--- TEST NOTIFICACION ESTUDIANTES ---\n")


    try:

        horario = reasignar_aula(
            db=db,
            horario_id=1,
            nueva_aula_id=3
        )


        print(
            "Horario actualizado:",
            horario.id
        )


        print("\nNotificaciones:\n")


        notificaciones = (
            db.query(Notificacion)
            .all()
        )


        for n in notificaciones:

            print("----------------")
            print("Usuario:", n.usuario_id)
            print("Mensaje:", n.mensaje)
            print("Tipo:", n.tipo_evento)
            print("Referencia:", n.referencia_id)



        print("\n✔ Test completado")


    finally:

        db.close()



if __name__ == "__main__":
    run()