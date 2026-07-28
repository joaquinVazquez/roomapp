from sqlalchemy.orm import Session
from app.models.horario import Horario


def build_horario_query(db: Session):
    return (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .filter(Horario.activo == True)
    )