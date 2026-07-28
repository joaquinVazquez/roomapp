from datetime import time
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.models.actividad_academica import ActividadAcademica
from app.models.horario import Horario


def run():

    db: Session = SessionLocal()

    try:
        print("\n🌱 Iniciando seed de datos...\n")

        # =========================
        # 1. PERSONA
        # =========================
        persona = db.query(Persona).filter_by(
            email="docente.prueba@unisa.edu.mx"
        ).first()

        if not persona:
            persona = Persona(
                nombre="Docente",
                apellido="Prueba",
                email="docente.prueba@unisa.edu.mx"
            )
            db.add(persona)
            db.commit()
            db.refresh(persona)
            print(f"✔ Persona creada ID: {persona.id}")
        else:
            print(f"ℹ Persona ya existe ID: {persona.id}")

        # =========================
        # 2. USUARIO
        # =========================
        usuario = db.query(Usuario).filter_by(
            email=persona.email
        ).first()

        if not usuario:
            usuario = Usuario(
                persona_id=persona.id,
                rol_id=3,  # DOCENTE
                email=persona.email,
                password_hash="testhash",
                activo=True
            )
            db.add(usuario)
            db.commit()
            db.refresh(usuario)
            print(f"✔ Usuario creado ID: {usuario.id}")
        else:
            print(f"ℹ Usuario ya existe ID: {usuario.id}")

        # =========================
        # 3. ACTIVIDAD ACADÉMICA
        # =========================
        actividad = db.query(ActividadAcademica).filter_by(
            grupo_id=1,
            materia_id=1,
            bloque="B2"
        ).first()

        if not actividad:
            actividad = ActividadAcademica(
                grupo_id=1,
                materia_id=1,
                docente_id=usuario.id,
                bloque="B2",
                activo=True
            )
            db.add(actividad)
            db.commit()
            db.refresh(actividad)
            print(f"✔ Actividad creada ID: {actividad.id}")
        else:
            print(f"ℹ Actividad ya existe ID: {actividad.id}")

        # =========================
        # 4. HORARIO (SIN CONFLICTO)
        # =========================
        from datetime import time

        horario = db.query(Horario).filter_by(
            actividad_academica_id=actividad.id,
            dia_semana_id=6,
            hora_inicio=time(10, 0),
            hora_fin=time(12, 0)
        ).first()

        if not horario:
            horario = Horario(
                actividad_academica_id=actividad.id,
                dia_semana_id=6,
                hora_inicio=time(10, 0),
                hora_fin=time(12, 0),
                aula_id=1,
                activo=True
            )
            db.add(horario)
            db.commit()
            db.refresh(horario)
            print(f"✔ Horario creado ID: {horario.id}")
        else:
            print(f"ℹ Horario ya existe ID: {horario.id}")


    except Exception as e:
        db.rollback()
        print("❌ Error en seed:", e)

    finally:
        db.close()

if __name__ == "__main__":
    run()