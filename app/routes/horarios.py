from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.horario import Horario
from app.models.usuario import Usuario

from app.schemas.horario import HorarioCreate, HorarioResponse

from app.services.horario_service import validar_conflictos
from app.services.horario_estudiante_service import obtener_horarios_estudiante
from app.services.horario_docente_service import obtener_horarios_docente

from app.core.security import get_current_user, require_roles

from app.schemas.horario_estudiante import HorarioEstudianteResponse
from app.schemas.horario_docente import HorarioDocenteResponse


router = APIRouter(prefix="/horarios", tags=["Horarios"])


# =========================
# CREAR HORARIO
# =========================
@router.post("/", response_model=HorarioResponse)
def crear_horario(
    horario: HorarioCreate,
    db: Session = Depends(get_db),
    user=Depends(require_roles("ADMINISTRADOR", "COORDINADOR_ACADEMICO"))
):
    validar_conflictos(db, horario)

    nuevo = Horario(**horario.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# =========================
# HORARIOS ESTUDIANTE
# =========================
@router.get(
    "/mis-horarios-estudiante",
    response_model=HorarioEstudianteResponse
)
def mis_horarios_estudiante(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_horarios_estudiante(db, current_user.id)


# =========================
# HORARIOS DOCENTE
# =========================
@router.get(
    "/mis-horarios-docente",
    response_model=HorarioDocenteResponse
)
def mis_horarios_docente(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return obtener_horarios_docente(db, current_user.id)