from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.horario import Horario
from app.schemas.horario import (
    HorarioCreate,
    HorarioUpdate,
    HorarioResponse
)


router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)


# CREAR HORARIO
@router.post(
    "/",
    response_model=HorarioResponse
)
def crear_horario(
    horario: HorarioCreate,
    db: Session = Depends(get_db)
):

    nuevo_horario = Horario(
        **horario.model_dump()
    )

    db.add(nuevo_horario)

    db.commit()

    db.refresh(nuevo_horario)

    return nuevo_horario



# LISTAR HORARIOS
@router.get(
    "/",
    response_model=list[HorarioResponse]
)
def listar_horarios(
    db: Session = Depends(get_db)
):

    horarios = (
        db.query(Horario)
        .filter(
            Horario.activo == True
        )
        .all()
    )

    return horarios



# OBTENER HORARIO POR ID
@router.get(
    "/{horario_id}",
    response_model=HorarioResponse
)
def obtener_horario(
    horario_id: int,
    db: Session = Depends(get_db)
):

    horario = (
        db.query(Horario)
        .filter(
            Horario.id == horario_id
        )
        .first()
    )


    if not horario:

        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    return horario



# ACTUALIZAR HORARIO
@router.put(
    "/{horario_id}",
    response_model=HorarioResponse
)
def actualizar_horario(
    horario_id: int,
    datos: HorarioUpdate,
    db: Session = Depends(get_db)
):

    horario = (
        db.query(Horario)
        .filter(
            Horario.id == horario_id
        )
        .first()
    )


    if not horario:

        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    for campo, valor in datos.model_dump(
        exclude_unset=True
    ).items():

        setattr(
            horario,
            campo,
            valor
        )


    db.commit()

    db.refresh(horario)

    return horario



# ELIMINACIÓN LÓGICA
@router.delete(
    "/{horario_id}"
)
def eliminar_horario(
    horario_id: int,
    db: Session = Depends(get_db)
):

    horario = (
        db.query(Horario)
        .filter(
            Horario.id == horario_id
        )
        .first()
    )


    if not horario:

        raise HTTPException(
            status_code=404,
            detail="Horario no encontrado"
        )


    horario.activo = False


    db.commit()


    return {
        "message": "Horario desactivado correctamente"
    }