from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.programa import Programa
from app.schemas.programa import (
    ProgramaCreate,
    ProgramaUpdate,
    ProgramaResponse,
)
from app.core.security import require_roles

router = APIRouter(
    prefix="/programas",
    tags=["Programas"]
)

@router.post(
    "/",
    response_model=ProgramaResponse
)
def create_programa(
    programa: ProgramaCreate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):
    existe = (
        db.query(Programa)
        .filter(Programa.clave == programa.clave)
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="La clave del programa ya existe."
        )

    nuevo = Programa(**programa.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


@router.get(
    "/",
    response_model=list[ProgramaResponse]
)
def get_programas(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):
    return db.query(Programa).all()


@router.get(
    "/{programa_id}",
    response_model=ProgramaResponse
)
def get_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):
    programa = db.query(Programa).filter(
        Programa.id == programa_id
    ).first()

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado."
        )

    return programa


@router.put(
    "/{programa_id}",
    response_model=ProgramaResponse
)
def update_programa(
    programa_id: int,
    datos: ProgramaUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):
    programa = db.query(Programa).filter(
        Programa.id == programa_id
    ).first()

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado."
        )

    for campo, valor in datos.model_dump(
        exclude_unset=True
    ).items():
        setattr(programa, campo, valor)

    db.commit()
    db.refresh(programa)

    return programa


@router.delete("/{programa_id}")
def delete_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):
    programa = db.query(Programa).filter(
        Programa.id == programa_id
    ).first()

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado."
        )

    db.delete(programa)
    db.commit()

    return {
        "message": "Programa eliminado correctamente."
    }