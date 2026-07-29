from datetime import datetime

from app.db.session import SessionLocal

from app.models.persona import Persona
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.grupo import Grupo
from app.models.inscripcion import Inscripcion
from app.models.periodo_academico import PeriodoAcademico

from app.core.security import hash_password


def run():

    db = SessionLocal()

    print("\n--- SEED INSCRIPCIONES ---\n")


    try:

        # =====================================
        # 1. BUSCAR ROL ESTUDIANTE
        # =====================================

        rol_estudiante = db.query(Rol).filter(
            Rol.nombre == "ESTUDIANTE"
        ).first()


        if not rol_estudiante:

            print("❌ No existe rol ESTUDIANTE")
            return


        print(
            "✔ Rol encontrado:",
            rol_estudiante.nombre
        )


        # =====================================
        # 2. BUSCAR GRUPO
        # =====================================

        grupo = db.query(Grupo).first()


        if not grupo:

            print("❌ No existen grupos")
            return


        print(
            "✔ Grupo:",
            grupo.nombre
        )


        # =====================================
        # 3. CREAR PERSONA
        # =====================================

        persona = Persona(
            nombre="Juan",
            apellido="Pérez",
            email="juan.estudiante@test.com"
        )


        db.add(persona)
        db.commit()
        db.refresh(persona)


        print(
            "✔ Persona creada:",
            persona.nombre
        )


        # =====================================
        # 4. CREAR USUARIO
        # =====================================

        usuario = Usuario(

            persona_id=persona.id,

            rol_id=rol_estudiante.id,

            email="juan.estudiante@test.com",

            password_hash=hash_password(
                "123456"
            )

        )


        db.add(usuario)
        db.commit()
        db.refresh(usuario)


        print(
            "✔ Usuario creado:",
            usuario.email
        )


        # =====================================
        # 5. CREAR INSCRIPCIÓN
        # =====================================

        inscripcion = Inscripcion(

            usuario_id=usuario.id,

            grupo_id=grupo.id,

            periodo_academico_id=grupo.periodo_academico_id

        )


        db.add(inscripcion)
        db.commit()
        db.refresh(inscripcion)


        print(
            "✔ Inscripción creada:",
            inscripcion.id
        )


        print("\n✔ Seed completado")


    except Exception as e:

        db.rollback()

        print(
            "❌ Error:",
            e
        )


    finally:

        db.close()



if __name__ == "__main__":
    run()