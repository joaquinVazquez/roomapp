from sqlalchemy.orm import Session

from app.models.inscripcion import Inscripcion
from app.models.usuario import Usuario


def obtener_estudiantes_por_grupo(
    db: Session,
    grupo_id: int
):

    return (
        db.query(Usuario)
        .join(
            Inscripcion,
            Usuario.id == Inscripcion.usuario_id
        )
        .filter(
            Inscripcion.grupo_id == grupo_id,
            Inscripcion.activo == True
        )
        .all()
    )