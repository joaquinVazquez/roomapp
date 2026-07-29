from app.db.session import SessionLocal

from app.services.inscripcion_service import (
    obtener_estudiantes_por_grupo
)


def run():

    db = SessionLocal()

    print("\n--- TEST ESTUDIANTES POR GRUPO ---\n")


    grupo_id = 1


    estudiantes = obtener_estudiantes_por_grupo(
        db,
        grupo_id
    )


    print(
        "Total estudiantes:",
        len(estudiantes)
    )


    for estudiante in estudiantes:

        print("----------------")
        print("Usuario ID:", estudiante.id)
        print("Email:", estudiante.email)


    print("\n✔ Test completado")


    db.close()



if __name__ == "__main__":
    run()