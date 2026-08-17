from sqlalchemy.orm import Session
from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.grupo import Grupo


def build_horario_query(db: Session):
    return (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(ActividadAcademica.grupo)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
    )