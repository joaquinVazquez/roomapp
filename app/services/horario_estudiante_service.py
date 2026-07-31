from sqlalchemy.orm import Session
from collections import defaultdict
from fastapi import HTTPException

from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.inscripcion import Inscripcion


def obtener_horarios_estudiante(db: Session, usuario_id: int):

    # =========================
    # VALIDAR INSCRIPCIÓN
    # =========================
    inscripciones = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.usuario_id == usuario_id,
            Inscripcion.activo == True
        )
        .all()
    )

    if len(inscripciones) == 0:
        return {"dias": []}

    if len(inscripciones) > 1:
        raise HTTPException(
            status_code=400,
            detail="El estudiante tiene múltiples inscripciones activas"
        )

    grupo_id = inscripciones[0].grupo_id

    # =========================
    # CONSULTAR HORARIOS
    # =========================
    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .filter(
            ActividadAcademica.grupo_id == grupo_id,
            Horario.activo == True
        )
        .order_by(Horario.dia_semana_id, Horario.hora_inicio)
        .all()
    )

    # =========================
    # FORMATEAR RESPUESTA
    # =========================
    resultado = defaultdict(list)

    for h in horarios:
        resultado[h.dia_semana.nombre].append({
            "hora": f"{h.hora_inicio} - {h.hora_fin}",
            "materia": h.actividad_academica.materia.nombre,
            "grupo": h.actividad_academica.grupo.nombre,
            "aula": h.aula.nombre if h.aula else "SIN ASIGNAR",
            "docente": h.actividad_academica.docente.persona.nombre
        })

    dias = []

    for dia, clases in resultado.items():
        dias.append({
            "dia": dia,
            "clases": clases
        })

    return {"dias": dias}