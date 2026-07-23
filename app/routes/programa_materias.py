from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.programa_materia import ProgramaMateria
from app.models.programa import Programa
from app.models.materia import Materia

from app.core.security import require_roles


router = APIRouter(
    prefix="/programas",
    tags=["Programa Materias"]
)


@router.post("/{programa_id}/materias/{materia_id}")
def asignar_materia(
    programa_id: int,
    materia_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    programa = (
        db.query(Programa)
        .filter(Programa.id == programa_id)
        .first()
    )

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado."
        )


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


    existe = (
        db.query(ProgramaMateria)
        .filter(
            ProgramaMateria.programa_id == programa_id,
            ProgramaMateria.materia_id == materia_id
        )
        .first()
    )


    if existe:
        raise HTTPException(
            status_code=400,
            detail="La materia ya está asignada al programa."
        )


    relacion = ProgramaMateria(
        programa_id=programa_id,
        materia_id=materia_id
    )


    db.add(relacion)
    db.commit()
    db.refresh(relacion)


    return {
        "message": "Materia asignada correctamente.",
        "programa_id": programa_id,
        "materia_id": materia_id
    }



@router.get("/{programa_id}/materias")
def obtener_materias_programa(
    programa_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    programa = (
        db.query(Programa)
        .filter(Programa.id == programa_id)
        .first()
    )


    if not programa:
        raise HTTPException(
            status_code=404,
            detail="Programa no encontrado."
        )


    materias = (
        db.query(Materia)
        .join(
            ProgramaMateria,
            ProgramaMateria.materia_id == Materia.id
        )
        .filter(
            ProgramaMateria.programa_id == programa_id
        )
        .all()
    )


    return materias



@router.delete(
    "/{programa_id}/materias/{materia_id}"
)
def quitar_materia(
    programa_id: int,
    materia_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    relacion = (
        db.query(ProgramaMateria)
        .filter(
            ProgramaMateria.programa_id == programa_id,
            ProgramaMateria.materia_id == materia_id
        )
        .first()
    )


    if not relacion:
        raise HTTPException(
            status_code=404,
            detail="La relación no existe."
        )


    db.delete(relacion)
    db.commit()


    return {
        "message": "Materia retirada del programa."
    }