from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.grupo import Grupo
from app.schemas.grupo import (
    GrupoCreate,
    GrupoUpdate,
    GrupoResponse
)
from app.core.security import require_roles


router = APIRouter(
    prefix="/grupos",
    tags=["Grupos"]
)


# 🔹 Crear grupo
@router.post(
    "/",
    response_model=GrupoResponse
)
def crear_grupo(
    grupo: GrupoCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    existente = db.query(Grupo).filter(
        Grupo.clave == grupo.clave
    ).first()

    if existente:
        raise HTTPException(
            status_code=400,
            detail="La clave del grupo ya existe."
        )

    nuevo = Grupo(**grupo.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# 🔹 Listar grupos
@router.get(
    "/",
    response_model=list[GrupoResponse]
)
def listar_grupos(
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):
    return db.query(Grupo).filter(
        Grupo.activo == True
    ).all()


# 🔹 Obtener uno
@router.get(
    "/{grupo_id}",
    response_model=GrupoResponse
)
def obtener_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    grupo = db.query(Grupo).filter(
        Grupo.id == grupo_id
    ).first()

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="Grupo no encontrado"
        )

    return grupo


# 🔹 Actualizar
@router.put(
    "/{grupo_id}",
    response_model=GrupoResponse
)
def actualizar_grupo(
    grupo_id: int,
    datos: GrupoUpdate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    grupo = db.query(Grupo).filter(
        Grupo.id == grupo_id
    ).first()

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="Grupo no encontrado"
        )

    for campo, valor in datos.model_dump(
        exclude_unset=True
    ).items():
        setattr(grupo, campo, valor)

    db.commit()
    db.refresh(grupo)

    return grupo


# 🔹 Eliminación lógica
@router.delete(
    "/{grupo_id}"
)
def eliminar_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):

    grupo = db.query(Grupo).filter(
        Grupo.id == grupo_id
    ).first()

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="Grupo no encontrado"
        )

    grupo.activo = False

    db.commit()

    return {
        "message": "Grupo desactivado correctamente"
    }