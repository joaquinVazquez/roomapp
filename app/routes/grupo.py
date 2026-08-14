from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.grupo import Grupo
from app.models.programa import Programa
from app.models.periodo_academico import PeriodoAcademico

from app.schemas.grupo import (
    GrupoCreate,
    GrupoUpdate,
    GrupoResponse
)

from app.core.security import require_roles


router = APIRouter(
    prefix="/grupos",
    tags=["Grupos"]
)


# ============================================================
# CREAR GRUPO
# ============================================================

@router.post(
    "/",
    response_model=GrupoResponse
)
def crear_grupo(
    grupo: GrupoCreate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    # --------------------------------------------------------
    # Validar programa
    # --------------------------------------------------------

    programa = (
        db.query(Programa)
        .filter(
            Programa.id == grupo.programa_id
        )
        .first()
    )

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="El programa académico no existe."
        )

    if not programa.activo:
        raise HTTPException(
            status_code=400,
            detail="El programa académico está inactivo."
        )

    # --------------------------------------------------------
    # Validar periodo académico
    # --------------------------------------------------------

    periodo = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.id
            == grupo.periodo_academico_id
        )
        .first()
    )

    if not periodo:
        raise HTTPException(
            status_code=404,
            detail="El periodo académico no existe."
        )

    if not periodo.activo:
        raise HTTPException(
            status_code=400,
            detail="El periodo académico está inactivo."
        )

    # --------------------------------------------------------
    # Validar grupo duplicado dentro del mismo periodo
    # --------------------------------------------------------

    existente = (
        db.query(Grupo)
        .filter(
            Grupo.clave == grupo.clave,
            Grupo.periodo_academico_id
            == grupo.periodo_academico_id
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=400,
            detail=(
                "Ya existe un grupo con esa clave "
                "en el periodo académico seleccionado."
            )
        )

    # --------------------------------------------------------
    # Crear grupo
    # --------------------------------------------------------

    nuevo = Grupo(
        **grupo.model_dump()
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# ============================================================
# LISTAR GRUPOS
# ============================================================

@router.get(
    "/",
    response_model=list[GrupoResponse]
)
def listar_grupos(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    return (
        db.query(Grupo)
        .filter(
            Grupo.activo == True
        )
        .order_by(Grupo.id)
        .all()
    )


# ============================================================
# OBTENER GRUPO
# ============================================================

@router.get(
    "/{grupo_id}",
    response_model=GrupoResponse
)
def obtener_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    grupo = (
        db.query(Grupo)
        .filter(
            Grupo.id == grupo_id
        )
        .first()
    )

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="Grupo no encontrado."
        )

    return grupo


# ============================================================
# ACTUALIZAR GRUPO
# ============================================================

@router.put(
    "/{grupo_id}",
    response_model=GrupoResponse
)
def actualizar_grupo(
    grupo_id: int,
    datos: GrupoUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    # --------------------------------------------------------
    # Buscar grupo
    # --------------------------------------------------------

    grupo = (
        db.query(Grupo)
        .filter(
            Grupo.id == grupo_id
        )
        .first()
    )

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="Grupo no encontrado."
        )

    cambios = datos.model_dump(
        exclude_unset=True
    )

    # --------------------------------------------------------
    # Determinar valores finales
    # --------------------------------------------------------

    programa_id = cambios.get(
        "programa_id",
        grupo.programa_id
    )

    periodo_id = cambios.get(
        "periodo_academico_id",
        grupo.periodo_academico_id
    )

    clave = cambios.get(
        "clave",
        grupo.clave
    )

    # --------------------------------------------------------
    # Validar programa
    # --------------------------------------------------------

    programa = (
        db.query(Programa)
        .filter(
            Programa.id == programa_id
        )
        .first()
    )

    if not programa:
        raise HTTPException(
            status_code=404,
            detail="El programa académico no existe."
        )

    if not programa.activo:
        raise HTTPException(
            status_code=400,
            detail="El programa académico está inactivo."
        )

    # --------------------------------------------------------
    # Validar periodo
    # --------------------------------------------------------

    periodo = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.id == periodo_id
        )
        .first()
    )

    if not periodo:
        raise HTTPException(
            status_code=404,
            detail="El periodo académico no existe."
        )

    if not periodo.activo:
        raise HTTPException(
            status_code=400,
            detail="El periodo académico está inactivo."
        )

    # --------------------------------------------------------
    # Validar duplicado
    #
    # La misma clave sí puede existir en otros periodos.
    # --------------------------------------------------------

    existente = (
        db.query(Grupo)
        .filter(
            Grupo.clave == clave,
            Grupo.periodo_academico_id == periodo_id,
            Grupo.id != grupo_id
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=400,
            detail=(
                "Ya existe otro grupo con esa clave "
                "en el periodo académico seleccionado."
            )
        )

    # --------------------------------------------------------
    # Aplicar cambios
    # --------------------------------------------------------

    for campo, valor in cambios.items():
        setattr(
            grupo,
            campo,
            valor
        )

    db.commit()
    db.refresh(grupo)

    return grupo


# ============================================================
# DESACTIVAR GRUPO
# ============================================================

@router.delete(
    "/{grupo_id}"
)
def eliminar_grupo(
    grupo_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    grupo = (
        db.query(Grupo)
        .filter(
            Grupo.id == grupo_id
        )
        .first()
    )

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="Grupo no encontrado."
        )

    # --------------------------------------------------------
    # No se elimina físicamente.
    # Se conserva el historial.
    # --------------------------------------------------------

    grupo.activo = False

    db.commit()

    return {
        "message": "Grupo desactivado correctamente."
    }