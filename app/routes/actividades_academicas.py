from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.actividad_academica import ActividadAcademica
from app.schemas.actividad_academica import (
    ActividadAcademicaCreate,
    ActividadAcademicaUpdate,
    ActividadAcademicaResponse
)
from app.core.security import require_roles


router = APIRouter(
    prefix="/actividades-academicas",
    tags=["Actividades Académicas"]
)


# 🔍 LISTAR
@router.get(
    "/",
    response_model=list[ActividadAcademicaResponse]
)
def get_actividades(
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):
    return db.query(ActividadAcademica).all()


# 🔍 DETALLE
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
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    return actividad


# ➕ CREAR
@router.post(
    "/",
    response_model=ActividadAcademicaResponse
)
def create_actividad(
    data: ActividadAcademicaCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    # Validar duplicado
    existe = db.query(ActividadAcademica).filter(
        ActividadAcademica.grupo_id == data.grupo_id,
        ActividadAcademica.materia_id == data.materia_id,
        ActividadAcademica.bloque == data.bloque,
        #ActividadAcademica.periodo_academico_id == data.periodo_academico_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="La actividad académica ya existe para ese grupo, materia, bloque y periodo."
        )

    nueva = ActividadAcademica(**data.model_dump())

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva


# ✏️ ACTUALIZAR
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
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(actividad, campo, valor)

    db.commit()
    db.refresh(actividad)

    return actividad


# 🧹 DELETE LÓGICO
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
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    actividad.activo = False

    db.commit()

    return {"message": "Actividad desactivada correctamente"}