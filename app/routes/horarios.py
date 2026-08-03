from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.horario import Horario
from app.models.usuario import Usuario
from app.models.actividad_academica import ActividadAcademica

from app.schemas.horario import HorarioCreate, HorarioResponse

from app.services.horario_service import validar_conflictos, reasignar_aula
from app.services.horario_query_service import build_horario_query
from app.services.horario_estudiante_service import obtener_horarios_estudiante
from app.services.horario_docente_service import obtener_horarios_docente

from app.core.security import get_current_user, require_roles
from app.services.horario_general_service import obtener_horarios_generales
from typing import Optional


router = APIRouter(prefix="/horarios", tags=["Horarios"])


# =========================
# CREAR HORARIO
# =========================
@router.post("/", response_model=HorarioResponse)
def crear_horario(
    horario: HorarioCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):
    validar_conflictos(db, horario)

    nuevo = Horario(**horario.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# =========================
# CONSULTA GENERAL
# =========================
@router.get("/general")
def get_horarios_generales(
    periodo_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles(
        "ADMINISTRADOR",
        "COORDINADOR_ACADEMICO",
        "PERSONAL_ADMINISTRATIVO"
    ))
):
    return obtener_horarios_generales(
        db,
        periodo_id=periodo_id
    )


# =========================
# MIS HORARIOS DOCENTE
# =========================
@router.get("/mis-horarios-docente")
def get_mis_horarios_docente(
    periodo_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("DOCENTE"))
):
    return obtener_horarios_docente(
        db,
        docente_id=user.id,
        periodo_id=periodo_id
    )


# =========================
# MIS HORARIOS ESTUDIANTE
# =========================
@router.get("/mis-horarios-estudiante")
def get_mis_horarios_estudiante(
    periodo_id: int | None = None,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ESTUDIANTE"))
):
    return obtener_horarios_estudiante(
        db,
        usuario_id=user.id,
        periodo_id=periodo_id
    )


# =========================
# POR DOCENTE
# =========================
@router.get("/docente/{docente_id}")
def horario_por_docente(
    docente_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    return (
        build_horario_query(db)
        .filter(ActividadAcademica.docente_id == docente_id)
        .all()
    )


# =========================
# POR GRUPO
# =========================
@router.get("/grupo/{grupo_id}")
def horario_por_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    return (
        build_horario_query(db)
        .filter(ActividadAcademica.grupo_id == grupo_id)
        .all()
    )


# =========================
# POR AULA
# =========================
@router.get("/aula/{aula_id}")
def horario_por_aula(
    aula_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    return (
        build_horario_query(db)
        .filter(Horario.aula_id == aula_id)
        .all()
    )


# =========================
# REASIGNAR AULA
# =========================
@router.put("/{horario_id}/reasignar-aula")
def cambiar_aula(
    horario_id: int,
    nueva_aula_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    horario = reasignar_aula(
        db=db,
        horario_id=horario_id,
        nueva_aula_id=nueva_aula_id
    )

    return {
        "message": "Aula reasignada correctamente",
        "horario_id": horario.id,
        "nueva_aula": horario.aula_id
    }