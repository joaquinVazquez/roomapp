from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.horario import Horario
from app.models.actividad_academica import ActividadAcademica
from app.models.grupo import Grupo
from app.models.periodo_academico import PeriodoAcademico

from app.services.periodo_service import get_periodo_activo


def obtener_horarios_docente(
    db: Session,
    docente_id: int,
    periodo_id: int | None = None
):

    # =========================
    # OBTENER PERIODO
    # =========================
    periodo = None

    if periodo_id:
        periodo = db.query(PeriodoAcademico).filter(
            PeriodoAcademico.id == periodo_id
        ).first()
    else:
        periodo = get_periodo_activo(db)

    if not periodo:
        return {"dias": []}

    # =========================
    # QUERY
    # =========================
    horarios = (
        db.query(Horario)
        .join(Horario.actividad_academica)
        .join(ActividadAcademica.grupo)
        .join(Horario.dia_semana)
        .outerjoin(Horario.aula)
        .filter(
            ActividadAcademica.docente_id == docente_id,
            Grupo.periodo_academico_id == periodo.id,
            Horario.activo == True
        )
        .order_by(
            Horario.dia_semana_id,
            Horario.hora_inicio
        )
        .all()
    )

    # =========================
    # FORMATEAR
    # =========================
    resultado = defaultdict(list)

    for h in horarios:
        resultado[h.dia_semana.nombre].append({
            "hora": f"{h.hora_inicio} - {h.hora_fin}",
            "materia": h.actividad_academica.materia.nombre,
            "grupo": h.actividad_academica.grupo.nombre,
            "aula": h.aula.nombre if h.aula else "SIN ASIGNAR"
        })

    return {
        "dias": [
            {"dia": dia, "clases": clases}
            for dia, clases in resultado.items()
        ]
    }