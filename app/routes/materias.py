from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.materia import Materia

from app.schemas.materia import (
    MateriaCreate,
    MateriaUpdate,
    MateriaResponse
)

from app.core.security import require_roles


router = APIRouter(
    prefix="/materias",
    tags=["Materias"]
)


@router.post(
    "/",
    response_model=MateriaResponse
)
def create_materia(
    materia: MateriaCreate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    existe = (
        db.query(Materia)
        .filter(Materia.clave == materia.clave)
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="La clave de materia ya existe."
        )


    nueva = Materia(
        **materia.model_dump()
    )

    db.add(nueva)
    db.commit()
    db.refresh(nueva)

    return nueva



@router.get(
    "/",
    response_model=list[MateriaResponse]
)
def get_materias(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    return (
        db.query(Materia)
        .all()
    )



@router.get(
    "/{materia_id}",
    response_model=MateriaResponse
)
def get_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    materia = (
        db.query(Materia)
        .filter(Materia.id == materia_id)
        .first()
    )

    if not materia:
        raise HTTPException(
            status_code=404,
            detail="Materia no encontrada."
        )

    return materia



@router.put(
    "/{materia_id}",
    response_model=MateriaResponse
)
def update_materia(
    materia_id: int,
    datos: MateriaUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    materia = (
        db.query(Materia)
        .filter(Materia.id == materia_id)
        .first()
    )

    if not materia:
        raise HTTPException(
            status_code=404,
            detail="Materia no encontrada."
        )


    for campo, valor in datos.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            materia,
            campo,
            valor
        )


    db.commit()
    db.refresh(materia)

    return materia



@router.delete(
    "/{materia_id}"
)
def delete_materia(
    materia_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    materia = (
        db.query(Materia)
        .filter(Materia.id == materia_id)
        .first()
    )

    if not materia:
        raise HTTPException(
            status_code=404,
            detail="Materia no encontrada."
        )


    db.delete(materia)
    db.commit()

    return {
        "message": "Materia eliminada correctamente."
    }