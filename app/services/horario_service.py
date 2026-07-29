from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.aula import Aula
from app.models.usuario import Usuario

from app.services.notificacion_service import crear_notificacion
from app.services.inscripcion_service import obtener_estudiantes_por_grupo


def validar_conflictos(db: Session, horario_data):

    if horario_data.hora_inicio >= horario_data.hora_fin:
        raise HTTPException(400, "Hora inicio debe ser menor a fin")

    actividad = db.query(ActividadAcademica).filter(
        ActividadAcademica.id == horario_data.actividad_academica_id
    ).first()

    if not actividad:
        raise HTTPException(404, "Actividad no encontrada")

    # Aula
    if horario_data.aula_id:
        conflicto = db.query(Horario).filter(
            Horario.aula_id == horario_data.aula_id,
            Horario.dia_semana_id == horario_data.dia_semana_id,
            Horario.activo == True,
            Horario.hora_inicio < horario_data.hora_fin,
            Horario.hora_fin > horario_data.hora_inicio
        ).first()

        if conflicto:
            raise HTTPException(400, "Aula ocupada")

    # Docente
    conflicto_docente = db.query(Horario).join(ActividadAcademica).filter(
        ActividadAcademica.docente_id == actividad.docente_id,
        Horario.dia_semana_id == horario_data.dia_semana_id,
        Horario.activo == True,
        Horario.hora_inicio < horario_data.hora_fin,
        Horario.hora_fin > horario_data.hora_inicio
    ).first()

    if conflicto_docente:
        raise HTTPException(400, "Docente ocupado")

    # Grupo
    conflicto_grupo = db.query(Horario).join(ActividadAcademica).filter(
        ActividadAcademica.grupo_id == actividad.grupo_id,
        Horario.dia_semana_id == horario_data.dia_semana_id,
        Horario.activo == True,
        Horario.hora_inicio < horario_data.hora_fin,
        Horario.hora_fin > horario_data.hora_inicio
    ).first()

    if conflicto_grupo:
        raise HTTPException(400, "Grupo ocupado")


def reasignar_aula(db: Session, horario_id: int, nueva_aula_id: int):

    horario = db.query(Horario).filter(Horario.id == horario_id).first()
    if not horario:
        raise HTTPException(404, "Horario no encontrado")

    aula = db.query(Aula).filter(Aula.id == nueva_aula_id).first()
    if not aula:
        raise HTTPException(404, "Aula no existe")

    conflicto = db.query(Horario).filter(
        Horario.aula_id == nueva_aula_id,
        Horario.dia_semana_id == horario.dia_semana_id,
        Horario.hora_inicio < horario.hora_fin,
        Horario.hora_fin > horario.hora_inicio,
        Horario.id != horario_id,
        Horario.activo == True
    ).first()

    if conflicto:
        raise HTTPException(400, "Aula ocupada")

    horario.aula_id = nueva_aula_id
    db.commit()
    db.refresh(horario)

    actividad = horario.actividad_academica

    # Docente
    crear_notificacion(
        db=db,
        usuario_id=actividad.docente_id,
        mensaje=f"Aula cambiada a {aula.nombre}",
        tipo_evento="CAMBIO_AULA",
        referencia_id=horario.id
    )

    # Estudiantes
    estudiantes = obtener_estudiantes_por_grupo(db, actividad.grupo_id)

    for e in estudiantes:
        crear_notificacion(
            db=db,
            usuario_id=e.id,
            mensaje=f"Tu clase cambió a {aula.nombre}",
            tipo_evento="CAMBIO_AULA",
            referencia_id=horario.id
        )

    return horario