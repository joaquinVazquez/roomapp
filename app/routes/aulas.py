from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.aula import Aula
from app.schemas.aula import (
    AulaCreate,
    AulaUpdate,
    AulaResponse,
)
from app.core.security import require_roles


router = APIRouter(
    prefix="/aulas",
    tags=["Aulas"]
)

@router.post(
    "/",
    response_model=AulaResponse
)
def create_aula(
    aula: AulaCreate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    aula_existente = (
        db.query(Aula)
        .filter(
            Aula.clave == aula.clave
        )
        .first()
    )

    if aula_existente:
        raise HTTPException(
            status_code=400,
            detail="La clave del aula ya existe."
        )

    nueva_aula = Aula(
        **aula.model_dump()
    )

    db.add(nueva_aula)

    db.commit()

    db.refresh(nueva_aula)

    return nueva_aula

@router.get(
    "/",
    response_model=list[AulaResponse]
)
def get_aulas(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    return db.query(Aula).all()

@router.get(
    "/{aula_id}",
    response_model=AulaResponse
)
def get_aula(
    aula_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    aula = (
        db.query(Aula)
        .filter(
            Aula.id == aula_id
        )
        .first()
    )

    if not aula:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada."
        )

    return aula