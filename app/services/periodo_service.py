from sqlalchemy.orm import Session

from app.models.periodo_academico import PeriodoAcademico


def get_periodo_activo(db: Session):

    periodo = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.activo == True
        )
        .first()
    )

    return periodo