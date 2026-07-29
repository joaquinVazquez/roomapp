from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.usuario import Usuario
from app.schemas.horario import (
    HorarioCreate,
    HorarioUpdate,
    HorarioResponse
)

from app.services.horario_service import validar_conflictos
from app.core.security import get_current_user
from app.services.horario_query_service import build_horario_query
from app.models.actividad_academica import ActividadAcademica
from app.services.horario_service import reasignar_aula
from app.core.deps import require_permission




router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)

# =========================
# CREAR HORARIO
# =========================
@router.post("/", response_model=HorarioResponse)
def crear_horario(
    horario: HorarioCreate,
    db: Session = Depends(get_db)
):
    validar_conflictos(db, horario)

    nuevo = Horario(**horario.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# =========================
# LISTAR
# =========================
@router.get("/", response_model=list[HorarioResponse])
def listar_horarios(db: Session = Depends(get_db)):
    return db.query(Horario).filter(Horario.activo == True).all()


# =========================
# MIS HORARIOS (DOCENTE - JWT)
# =========================
@router.get("/mis-horarios")
def mis_horarios(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .filter(
            ActividadAcademica.docente_id == current_user.id,
            Horario.activo == True
        )
        .all()
    )

    resultado = []

    for h in horarios:
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


# =========================
# POR DOCENTE (ADMIN)
# =========================
@router.get("/docente/{docente_id}")
def horario_por_docente(
    docente_id: int,
    db: Session = Depends(get_db)
):

    horarios = (
        build_horario_query(db)
        .filter(ActividadAcademica.docente_id == docente_id)
        .order_by(Horario.dia_semana_id, Horario.hora_inicio)
        .all()
    )

    resultado = []

    for h in horarios:
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


# =========================
# POR GRUPO
# =========================
@router.get("/grupo/{grupo_id}")
def horario_por_grupo(
    grupo_id: int,
    db: Session = Depends(get_db)
):

    horarios = (
        build_horario_query(db)
        .filter(ActividadAcademica.grupo_id == grupo_id)
        .order_by(Horario.dia_semana_id, Horario.hora_inicio)
        .all()
    )

    resultado = []

    for h in horarios:
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


# =========================
# POR AULA
# =========================
@router.get("/aula/{aula_id}")
def horario_por_aula(
    aula_id: int,
    db: Session = Depends(get_db)
):

    horarios = (
        build_horario_query(db)
        .filter(Horario.aula_id == aula_id)
        .order_by(Horario.dia_semana_id, Horario.hora_inicio)
        .all()
    )

    resultado = []

    for h in horarios:
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

@router.put("/{horario_id}/reasignar-aula")
@router.put("/{horario_id}/reasignar-aula")
def cambiar_aula(
    horario_id: int,
    nueva_aula_id: int,
    db: Session = Depends(get_db),
    usuario=Depends(require_permission("REASIGNAR_AULA"))
):
    horario = reasignar_aula(db, horario_id, nueva_aula_id)

    return {
        "message": "Aula reasignada correctamente",
        "horario_id": horario.id,
        "nueva_aula": horario.aula_id
    }