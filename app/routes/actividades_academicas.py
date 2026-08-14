from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.actividad_academica import ActividadAcademica
from app.models.periodo_academico import PeriodoAcademico
from app.models.grupo import Grupo
from app.models.materia import Materia
from app.models.usuario import Usuario

from app.schemas.actividad_academica import (
    ActividadAcademicaCreate,
    ActividadAcademicaUpdate,
    ActividadAcademicaResponse,
)

from app.core.security import require_roles


router = APIRouter(
    prefix="/actividades-academicas",
    tags=["Actividades Académicas"]
)


# ============================================================
# LISTAR
# ============================================================

@router.get(
    "/",
    response_model=list[ActividadAcademicaResponse]
)
def get_actividades(
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):
    return (
        db.query(ActividadAcademica)
        .filter(ActividadAcademica.activo == True)
        .order_by(ActividadAcademica.id)
        .all()
    )


# ============================================================
# OBTENER POR ID
# ============================================================

@router.get(
    "/{actividad_id}",
    response_model=ActividadAcademicaResponse
)
def get_actividad(
    actividad_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    actividad = db.query(ActividadAcademica).filter(
        ActividadAcademica.id == actividad_id
    ).first()

    if not actividad:
        raise HTTPException(404, "Actividad académica no encontrada")

    return actividad


# ============================================================
# CREAR
# ============================================================

@router.post(
    "/",
    response_model=ActividadAcademicaResponse
)
def create_actividad(
    data: ActividadAcademicaCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    # 🔹 PERIODO
    periodo = db.query(PeriodoAcademico).filter(
        PeriodoAcademico.id == data.periodo_academico_id
    ).first()

    if not periodo:
        raise HTTPException(404, "El periodo académico no existe")

    if not periodo.activo:
        raise HTTPException(400, "El periodo académico está inactivo")

    # 🔹 GRUPO
    grupo = db.query(Grupo).filter(
        Grupo.id == data.grupo_id
    ).first()

    if not grupo:
        raise HTTPException(404, "El grupo no existe")

    # 🔥 VALIDACIÓN CLAVE
    if grupo.periodo_academico_id != data.periodo_academico_id:
        raise HTTPException(
            400,
            "El grupo no pertenece al periodo académico seleccionado"
        )

    # 🔹 MATERIA
    materia = db.query(Materia).filter(
        Materia.id == data.materia_id
    ).first()

    if not materia:
        raise HTTPException(404, "La materia no existe")

    # 🔹 DOCENTE
    docente = db.query(Usuario).filter(
        Usuario.id == data.docente_id
    ).first()

    if not docente:
        raise HTTPException(404, "El docente no existe")

    if not docente.activo:
        raise HTTPException(400, "El docente está inactivo")

    # 🔹 DUPLICADO
    existe = db.query(ActividadAcademica).filter(
        ActividadAcademica.grupo_id == data.grupo_id,
        ActividadAcademica.materia_id == data.materia_id,
        ActividadAcademica.bloque == data.bloque,
        ActividadAcademica.periodo_academico_id == data.periodo_academico_id
    ).first()

    if existe:
        raise HTTPException(
            400,
            "La actividad académica ya existe para ese grupo, materia, bloque y periodo"
        )

    nueva = ActividadAcademica(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# ============================================================
# ACTUALIZAR
# ============================================================

@router.put(
    "/{actividad_id}",
    response_model=ActividadAcademicaResponse
)
def update_actividad(
    actividad_id: int,
    data: ActividadAcademicaUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    actividad = db.query(ActividadAcademica).filter(
        ActividadAcademica.id == actividad_id
    ).first()

    if not actividad:
        raise HTTPException(404, "Actividad académica no encontrada")

    datos = data.model_dump(exclude_unset=True)

    # Valores finales
    grupo_id = datos.get("grupo_id", actividad.grupo_id)
    materia_id = datos.get("materia_id", actividad.materia_id)
    bloque = datos.get("bloque", actividad.bloque)
    periodo_id = datos.get("periodo_academico_id", actividad.periodo_academico_id)

    # 🔹 VALIDAR PERIODO
    periodo = db.query(PeriodoAcademico).filter(
        PeriodoAcademico.id == periodo_id
    ).first()

    if not periodo:
        raise HTTPException(404, "El periodo académico no existe")

    if not periodo.activo:
        raise HTTPException(400, "El periodo académico está inactivo")

    # 🔹 VALIDAR GRUPO
    grupo = db.query(Grupo).filter(Grupo.id == grupo_id).first()

    if not grupo:
        raise HTTPException(404, "El grupo no existe")

    if grupo.periodo_academico_id != periodo_id:
        raise HTTPException(
            400,
            "El grupo no pertenece al periodo académico seleccionado"
        )

    # 🔹 VALIDAR DUPLICADO
    existe = db.query(ActividadAcademica).filter(
        ActividadAcademica.grupo_id == grupo_id,
        ActividadAcademica.materia_id == materia_id,
        ActividadAcademica.bloque == bloque,
        ActividadAcademica.periodo_academico_id == periodo_id,
        ActividadAcademica.id != actividad_id
    ).first()

    if existe:
        raise HTTPException(
            400,
            "Ya existe otra actividad académica con los mismos datos"
        )

    # 🔹 ACTUALIZAR
    for campo, valor in datos.items():
        setattr(actividad, campo, valor)

    db.commit()
    db.refresh(actividad)

    return actividad


# ============================================================
# ELIMINACIÓN LÓGICA
# ============================================================

@router.delete("/{actividad_id}")
def delete_actividad(
    actividad_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    actividad = db.query(ActividadAcademica).filter(
        ActividadAcademica.id == actividad_id
    ).first()

    if not actividad:
        raise HTTPException(404, "Actividad académica no encontrada")

    actividad.activo = False

    db.commit()

    return {"message": "Actividad académica desactivada correctamente"}