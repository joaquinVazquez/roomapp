from sqlalchemy.orm import Session
from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from fastapi import HTTPException
from app.models.aula import Aula


def validar_conflictos(db: Session, horario_data):

    # =========================
    # VALIDAR RANGO DE HORAS
    # =========================
    if horario_data.hora_inicio >= horario_data.hora_fin:
        raise HTTPException(
            status_code=400,
            detail="La hora de inicio debe ser menor a la hora de fin"
        )

    # =========================
    # OBTENER ACTIVIDAD
    # =========================
    actividad = db.query(ActividadAcademica).filter(
        ActividadAcademica.id == horario_data.actividad_academica_id
    ).first()

    if not actividad:
        raise HTTPException(
            status_code=404,
            detail="Actividad académica no encontrada"
        )

    # =========================
    # CONFLICTO DE AULA
    # =========================
    if horario_data.aula_id is not None:

        conflicto_aula = db.query(Horario).filter(
            Horario.aula_id == horario_data.aula_id,
            Horario.dia_semana_id == horario_data.dia_semana_id,
            Horario.activo == True,
            Horario.hora_inicio < horario_data.hora_fin,
            Horario.hora_fin > horario_data.hora_inicio
        ).first()

        if conflicto_aula:
            raise HTTPException(
                status_code=400,
                detail="Conflicto de horario: el aula ya está ocupada en ese horario"
            )

    # =========================
    # CONFLICTO DE DOCENTE
    # =========================
    conflicto_docente = db.query(Horario).join(
        ActividadAcademica
    ).filter(
        ActividadAcademica.docente_id == actividad.docente_id,
        Horario.dia_semana_id == horario_data.dia_semana_id,
        Horario.activo == True,
        Horario.hora_inicio < horario_data.hora_fin,
        Horario.hora_fin > horario_data.hora_inicio
    ).first()

    if conflicto_docente:
        raise HTTPException(
            status_code=400,
            detail="Conflicto: el docente ya tiene clase en ese horario"
        )

    # =========================
    # CONFLICTO DE GRUPO
    # =========================
    conflicto_grupo = db.query(Horario).join(
        ActividadAcademica
    ).filter(
        ActividadAcademica.grupo_id == actividad.grupo_id,
        Horario.dia_semana_id == horario_data.dia_semana_id,
        Horario.activo == True,
        Horario.hora_inicio < horario_data.hora_fin,
        Horario.hora_fin > horario_data.hora_inicio
    ).first()

    if conflicto_grupo:
        raise HTTPException(
            status_code=400,
            detail="Conflicto: el grupo ya tiene clase en ese horario"
        )

def obtener_horarios_por_docente(db, docente_id):
    return (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .filter(Horario.actividad_academica.has(docente_id=docente_id))
        .all()
    )

def reasignar_aula(db: Session, horario_id: int, nueva_aula_id: int):

    horario = db.query(Horario).filter(Horario.id == horario_id).first()

    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    aula = (
    db.query(Aula)
    .filter(Aula.id == nueva_aula_id)
    .first()
    )

    if not aula:
        raise HTTPException(
            status_code=404,
            detail="El aula seleccionada no existe"
        )

    
    # 🔥 VALIDAR CONFLICTO DE AULA
    conflicto = (
        db.query(Horario)
        .filter(
            Horario.aula_id == nueva_aula_id,
            Horario.dia_semana_id == horario.dia_semana_id,
            Horario.hora_inicio < horario.hora_fin,
            Horario.hora_fin > horario.hora_inicio,
            Horario.id != horario_id,
            Horario.activo == True
        )
        .first()
    )

    if conflicto:
        raise HTTPException(
            status_code=400,
            detail="Conflicto: el aula ya está ocupada en ese horario"
        )

    # 🔁 REASIGNAR
    horario.aula_id = nueva_aula_id

    db.commit()
    db.refresh(horario)

    return horario