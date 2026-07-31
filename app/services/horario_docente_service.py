from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.grupo import Grupo

from app.services.periodo_service import get_periodo_activo


def obtener_horarios_docente(
    db: Session,
    docente_id: int
):

    # 🔹 Obtener periodo activo
    periodo = get_periodo_activo(db)

    if not periodo:
        return {"dias": []}

    # 🔹 Query filtrado por docente + periodo
    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(ActividadAcademica.grupo)  # 🔥 clave
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .filter(
            ActividadAcademica.docente_id == docente_id,
            Grupo.periodo_academico_id == periodo.id,  # 🔥 filtro nuevo
            Horario.activo == True
        )
        .order_by(
            Horario.dia_semana_id,
            Horario.hora_inicio
        )
        .all()
    )

    resultado = defaultdict(list)

    for h in horarios:
        resultado[h.dia_semana.nombre].append({

            "hora": f"{h.hora_inicio} - {h.hora_fin}",
            "materia": h.actividad_academica.materia.nombre,
            "grupo": h.actividad_academica.grupo.nombre,
            "aula": h.aula.nombre if h.aula else "SIN ASIGNAR"
        })

    response = []

    for dia, clases in resultado.items():
        response.append({
            "dia": dia,
            "clases": clases
        })

    return {
        "dias": response
    }