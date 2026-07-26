from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.horario_service import validar_conflictos

from app.db.session import get_db
from app.models.horario import Horario
from app.schemas.horario import (
    HorarioCreate,
    HorarioUpdate,
    HorarioResponse
)


router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)


# CREAR HORARIO
@router.post(
    "/",
    response_model=HorarioResponse
)

@router.post(
    "/",
    response_model=HorarioResponse
)
def crear_horario(
    horario: HorarioCreate,
    db: Session = Depends(get_db)
):

    # 🔥 VALIDACIÓN CENTRALIZADA
    validar_conflictos(db, horario)

    nuevo_horario = Horario(
        **horario.model_dump()
    )

    db.add(nuevo_horario)
    db.commit()
    db.refresh(nuevo_horario)

    return nuevo_horario



# LISTAR HORARIOS
@router.get(
    "/",
    response_model=list[HorarioResponse]
)
def listar_horarios(
    db: Session = Depends(get_db)
):

    horarios = (
        db.query(Horario)
        .filter(
            Horario.activo == True
        )
        .all()
    )

    return horarios



# OBTENER HORARIO POR ID
@router.get(
    "/{horario_id}",
    response_model=HorarioResponse
)
def obtener_horario(
    horario_id: int,
    db: Session = Depends(get_db)
):

    horario = (
        db.query(Horario)
        .filter(
            Horario.id == horario_id
        )
        .first()
    )


    if not horario:

        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    return horario



# ACTUALIZAR HORARIO
@router.put(
    "/{horario_id}",
    response_model=HorarioResponse
)
def actualizar_horario(
    horario_id: int,
    datos: HorarioUpdate,
    db: Session = Depends(get_db)
):

    horario = (
        db.query(Horario)
        .filter(
            Horario.id == horario_id
        )
        .first()
    )


    if not horario:

        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    for campo, valor in datos.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            horario,
            campo,
            valor
        )


    db.commit()

    db.refresh(horario)

    return horario



# ELIMINACIÓN LÓGICA
@router.delete(
    "/{horario_id}"
)
def eliminar_horario(
    horario_id: int,
    db: Session = Depends(get_db)
):

    horario = (
        db.query(Horario)
        .filter(
            Horario.id == horario_id
        )
        .first()
    )


    if not horario:

        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    horario.activo = False


    db.commit()


    return {
        "message": "Horario desactivado correctamente"
    }

@router.get("/docente/{docente_id}")
def horario_por_docente(
    docente_id: int,
    db: Session = Depends(get_db)
):

    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .all()
    )

    resultado = []

    for h in horarios:

        if h.actividad_academica.docente_id != docente_id:
            continue

        resultado.append({
            "id": h.id,
            "dia": h.dia_semana.nombre,
            "hora_inicio": str(h.hora_inicio),
            "hora_fin": str(h.hora_fin),
            "aula": h.aula.nombre if h.aula else None,
            "materia": h.actividad_academica.materia.nombre,
            "grupo": h.actividad_academica.grupo.nombre,
            "docente": h.actividad_academica.docente.persona.nombre
        })

    return resultado

@router.get("/grupo/{grupo_id}")
def horario_por_grupo(
    grupo_id: int,
    db: Session = Depends(get_db)
):

    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .all()
    )

    resultado = []

    for h in horarios:

        if h.actividad_academica.grupo_id != grupo_id:
            continue

        resultado.append({
            "id": h.id,
            "dia": h.dia_semana.nombre,
            "hora_inicio": str(h.hora_inicio),
            "hora_fin": str(h.hora_fin),
            "aula": h.aula.nombre if h.aula else None,
            "materia": h.actividad_academica.materia.nombre,
            "grupo": h.actividad_academica.grupo.nombre,
            "docente": h.actividad_academica.docente.persona.nombre
        })

    return resultado

@router.get("/aula/{aula_id}")
def horario_por_aula(
    aula_id: int,
    db: Session = Depends(get_db)
):

    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .all()
    )

    resultado = []

    for h in horarios:

        if h.aula_id != aula_id:
            continue

        resultado.append({
            "id": h.id,
            "dia": h.dia_semana.nombre,
            "hora_inicio": str(h.hora_inicio),
            "hora_fin": str(h.hora_fin),
            "aula": h.aula.nombre if h.aula else None,
            "materia": h.actividad_academica.materia.nombre,
            "grupo": h.actividad_academica.grupo.nombre,
            "docente": h.actividad_academica.docente.persona.nombre
        })

    return resultado