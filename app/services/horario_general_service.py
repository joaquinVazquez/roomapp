from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.horario import Horario


def obtener_horarios_generales(
    db: Session
):

    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .filter(
            Horario.activo == True
        )
        .order_by(
            Horario.dia_semana_id,
            Horario.hora_inicio
        )
        .all()
    )


    resultado = defaultdict(list)


    for h in horarios:

        resultado[
            h.dia_semana.nombre
        ].append({

            "hora":
            f"{h.hora_inicio} - {h.hora_fin}",

            "materia":
            h.actividad_academica.materia.nombre,

            "grupo":
            h.actividad_academica.grupo.nombre,

            "docente":
            h.actividad_academica.docente.persona.nombre,

            "aula":
            h.aula.nombre
            if h.aula
            else "SIN ASIGNAR"

        })


    return {

        "horarios":[
            {
                "dia": dia,
                "clases": clases
            }
            for dia, clases in resultado.items()
        ]

    }