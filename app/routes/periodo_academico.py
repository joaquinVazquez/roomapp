from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.periodo_academico import PeriodoAcademico
from app.schemas.periodo_academico import (
    PeriodoAcademicoCreate,
    PeriodoAcademicoUpdate,
    PeriodoAcademicoResponse,
)
from app.core.security import require_roles


router = APIRouter(
    prefix="/periodos-academicos",
    tags=["Periodos Académicos"]
)


@router.post(
    "/",
    response_model=PeriodoAcademicoResponse
)


@router.get(
    "/",
    response_model=list[PeriodoAcademicoResponse]
)
def get_periodos_academicos(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    return (
        db.query(PeriodoAcademico)
        .order_by(
            PeriodoAcademico.fecha_inicio
        )
        .all()
    )


def create_periodo_academico(
    periodo: PeriodoAcademicoCreate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    periodo_existente = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.clave == periodo.clave
        )
        .first()
    )

    if periodo_existente:

        raise HTTPException(
            status_code=400,
            detail="La clave del periodo académico ya existe."
        )

    nuevo_periodo = PeriodoAcademico(
        **periodo.model_dump()
    )

    db.add(nuevo_periodo)

    db.commit()

    db.refresh(nuevo_periodo)

    return nuevo_periodo


@router.get(
    "/{periodo_id}",
    response_model=PeriodoAcademicoResponse
)
def get_periodo_academico(
    periodo_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    periodo_db = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.id == periodo_id
        )
        .first()
    )

    if not periodo_db:

        raise HTTPException(
            status_code=404,
            detail="Periodo académico no encontrado."
        )

    return periodo_db

@router.put(
    "/{periodo_id}",
    response_model=PeriodoAcademicoResponse
)
def update_periodo_academico(
    periodo_id: int,
    datos: PeriodoAcademicoUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    periodo_db = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.id == periodo_id
        )
        .first()
    )

    if not periodo_db:

        raise HTTPException(
            status_code=404,
            detail="Periodo académico no encontrado."
        )

    if (
        datos.clave
        and datos.clave != periodo_db.clave
    ):

        periodo_existente = (
            db.query(PeriodoAcademico)
            .filter(
                PeriodoAcademico.clave == datos.clave
            )
            .first()
        )

        if periodo_existente:

            raise HTTPException(
                status_code=400,
                detail="La clave del periodo académico ya existe."
            )

    for campo, valor in datos.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            periodo_db,
            campo,
            valor
        )

    db.commit()

    db.refresh(periodo_db)

    return periodo_db

@router.delete(
    "/{periodo_id}"
)
def delete_periodo_academico(
    periodo_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    ),
):

    periodo_db = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.id == periodo_id
        )
        .first()
    )

    if not periodo_db:

        raise HTTPException(
            status_code=404,
            detail="Periodo académico no encontrado."
        )

    db.delete(periodo_db)

    db.commit()

    return {
        "message": "Periodo académico eliminado correctamente."
    }