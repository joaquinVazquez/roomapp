from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.aula import Aula
from app.models.usuario import Usuario

from app.services.notificacion_service import crear_notificacion
from app.services.inscripcion_service import obtener_estudiantes_por_grupo


# ==========================================
# VALIDAR CONFLICTOS DE HORARIO
# ==========================================
def validar_conflictos(db: Session, horario_data):

    if horario_data.hora_inicio >= horario_data.hora_fin:
        raise HTTPException(
            status_code=400,
            detail="La hora de inicio debe ser menor a la hora de fin"
        )


    actividad = db.query(ActividadAcademica).filter(
        ActividadAcademica.id == horario_data.actividad_academica_id
    ).first()


    if not actividad:
        raise HTTPException(
            status_code=404,
            detail="Actividad académica no encontrada"
        )


    # =========================
    # CONFLICTO AULA
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
                detail="Conflicto de horario: el aula ya está ocupada"
            )


    # =========================
    # CONFLICTO DOCENTE
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
            detail="Conflicto: el docente ya tiene clase"
        )


    # =========================
    # CONFLICTO GRUPO
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
            detail="Conflicto: el grupo ya tiene clase"
        )



# ==========================================
# OBTENER HORARIOS POR DOCENTE
# ==========================================
def obtener_horarios_por_docente(
    db: Session,
    docente_id: int
):

    return (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .filter(
            Horario.actividad_academica.has(
                docente_id=docente_id
            )
        )
        .all()
    )



# ==========================================
# REASIGNAR AULA
# ==========================================
def reasignar_aula(
    db: Session,
    horario_id: int,
    nueva_aula_id: int
):

    # =========================
    # BUSCAR HORARIO
    # =========================
    horario = db.query(Horario).filter(
        Horario.id == horario_id
    ).first()


    if not horario:
        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    # =========================
    # BUSCAR AULA
    # =========================
    aula = db.query(Aula).filter(
        Aula.id == nueva_aula_id
    ).first()


    if not aula:
        raise HTTPException(
            status_code=404,
            detail="El aula seleccionada no existe"
        )



    # =========================
    # VALIDAR CONFLICTO AULA
    # =========================
    conflicto = db.query(Horario).filter(
        Horario.aula_id == nueva_aula_id,
        Horario.dia_semana_id == horario.dia_semana_id,
        Horario.hora_inicio < horario.hora_fin,
        Horario.hora_fin > horario.hora_inicio,
        Horario.id != horario_id,
        Horario.activo == True
    ).first()


    if conflicto:
        raise HTTPException(
            status_code=400,
            detail="Conflicto: el aula ya está ocupada"
        )



    # =========================
    # ACTUALIZAR AULA
    # =========================
    horario.aula_id = nueva_aula_id


    db.commit()

    db.refresh(horario)



    # =========================
    # NOTIFICACIONES
    # =========================

    actividad = horario.actividad_academica


    if actividad:


        # -------------------------
        # 1. DOCENTE
        # -------------------------

        crear_notificacion(
            db=db,
            usuario_id=actividad.docente_id,
            mensaje=(
                f"Tu clase ha sido cambiada "
                f"al aula {aula.nombre}"
            ),
            tipo_evento="CAMBIO_AULA",
            referencia_id=horario.id
        )



        # -------------------------
        # 2. COORDINADORES
        # -------------------------

        coordinadores = db.query(Usuario).filter(
            Usuario.rol_id == 2,
            Usuario.activo == True
        ).all()


        for coord in coordinadores:

            crear_notificacion(
                db=db,
                usuario_id=coord.id,
                mensaje=(
                    f"Se reasignó el aula "
                    f"del horario {horario.id}"
                ),
                tipo_evento="CAMBIO_AULA",
                referencia_id=horario.id
            )



        # -------------------------
        # 3. ESTUDIANTES
        # -------------------------

        estudiantes = obtener_estudiantes_por_grupo(
            db=db,
            grupo_id=actividad.grupo_id
        )


        for estudiante in estudiantes:

            crear_notificacion(
                db=db,
                usuario_id=estudiante.id,
                mensaje=(
                    f"Tu clase cambió "
                    f"al aula {aula.nombre}"
                ),
                tipo_evento="CAMBIO_AULA",
                referencia_id=horario.id
            )



    return horario