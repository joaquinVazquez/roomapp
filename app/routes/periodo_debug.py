from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.periodo_service import get_periodo_activo

router = APIRouter(tags=["Debug"])


@router.get("/debug/periodo-activo")
def debug_periodo(db: Session = Depends(get_db)):

    periodo = get_periodo_activo(db)

    if not periodo:
        return {"message": "No hay periodo activo"}

    return {
        "id": periodo.id,
        "nombre": periodo.nombre,
        "activo": periodo.activo
    }