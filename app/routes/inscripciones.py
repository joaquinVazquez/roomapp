from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.inscripcion import Inscripcion
from app.models.usuario import Usuario
from app.models.grupo import Grupo
from app.models.periodo_academico import PeriodoAcademico

from app.schemas.inscripcion import (
    InscripcionCreate,
    InscripcionUpdate,
    InscripcionResponse,
)

from app.core.security import require_roles


router = APIRouter(
    prefix="/inscripciones",
    tags=["Inscripciones"]
)


# ============================================================
# CREAR INSCRIPCIÓN
# ============================================================

@router.post(
    "/",
    response_model=InscripcionResponse
)
def crear_inscripcion(
    datos: InscripcionCreate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    # --------------------------------------------------------
    # 1. Validar estudiante
    # --------------------------------------------------------

    usuario = (
        db.query(Usuario)
        .filter(
            Usuario.id == datos.usuario_id
        )
        .first()
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="El usuario no existe"
        )

    if not usuario.activo:
        raise HTTPException(
            status_code=400,
            detail="El usuario está inactivo"
        )

    if not usuario.rol or usuario.rol.nombre != "ESTUDIANTE":
        raise HTTPException(
            status_code=400,
            detail="El usuario seleccionado no tiene el rol ESTUDIANTE"
        )

    # --------------------------------------------------------
    # 2. Validar periodo
    # --------------------------------------------------------

    periodo = (
        db.query(PeriodoAcademico)
        .filter(
            PeriodoAcademico.id
            == datos.periodo_academico_id
        )
        .first()
    )

    if not periodo:
        raise HTTPException(
            status_code=404,
            detail="El periodo académico no existe"
        )

    if not periodo.activo:
        raise HTTPException(
            status_code=400,
            detail="El periodo académico está inactivo"
        )

    # --------------------------------------------------------
    # 3. Validar grupo
    # --------------------------------------------------------

    grupo = (
        db.query(Grupo)
        .filter(
            Grupo.id == datos.grupo_id
        )
        .first()
    )

    if not grupo:
        raise HTTPException(
            status_code=404,
            detail="El grupo no existe"
        )

    if not grupo.activo:
        raise HTTPException(
            status_code=400,
            detail="El grupo está inactivo"
        )

    # --------------------------------------------------------
    # 4. Validar que grupo y periodo coincidan
    # --------------------------------------------------------

    if grupo.periodo_academico_id != datos.periodo_academico_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "El grupo no pertenece al periodo "
                "académico seleccionado"
            )
        )

    # --------------------------------------------------------
    # 5. Comprobar inscripción activa existente
    # --------------------------------------------------------

    existente = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.usuario_id == datos.usuario_id,
            Inscripcion.periodo_academico_id
            == datos.periodo_academico_id,
            Inscripcion.activo == True
        )
        .first()
    )

    if existente:
        raise HTTPException(
            status_code=400,
            detail=(
                "El estudiante ya tiene una inscripción "
                "activa en este periodo académico"
            )
        )

    # --------------------------------------------------------
    # 6. Crear inscripción
    # --------------------------------------------------------

    nueva = Inscripcion(
        usuario_id=datos.usuario_id,
        grupo_id=datos.grupo_id,
        periodo_academico_id=datos.periodo_academico_id,
        activo=True
    )

    db.add(nueva)

    try:
        db.commit()
        db.refresh(nueva)

    except Exception:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="No fue posible crear la inscripción"
        )

    return nueva


# ============================================================
# LISTAR INSCRIPCIONES
# ============================================================

@router.get(
    "/",
    response_model=list[InscripcionResponse]
)
def listar_inscripciones(
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    return (
        db.query(Inscripcion)
        .order_by(Inscripcion.id)
        .all()
    )


# ============================================================
# OBTENER INSCRIPCIÓN
# ============================================================

@router.get(
    "/{inscripcion_id}",
    response_model=InscripcionResponse
)
def obtener_inscripcion(
    inscripcion_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    inscripcion = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.id == inscripcion_id
        )
        .first()
    )

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    return inscripcion


# ============================================================
# ACTUALIZAR INSCRIPCIÓN
# ============================================================

@router.put(
    "/{inscripcion_id}",
    response_model=InscripcionResponse
)
def actualizar_inscripcion(
    inscripcion_id: int,
    datos: InscripcionUpdate,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    inscripcion = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.id == inscripcion_id
        )
        .first()
    )

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    cambios = datos.model_dump(
        exclude_unset=True
    )

    grupo_id = cambios.get(
        "grupo_id",
        inscripcion.grupo_id
    )

    periodo_id = cambios.get(
        "periodo_academico_id",
        inscripcion.periodo_academico_id
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
            detail="El periodo académico no existe"
        )

    if not periodo.activo:
        raise HTTPException(
            status_code=400,
            detail="El periodo académico está inactivo"
        )

    # --------------------------------------------------------
    # Validar grupo
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
            detail="El grupo no existe"
        )

    if not grupo.activo:
        raise HTTPException(
            status_code=400,
            detail="El grupo está inactivo"
        )

    if grupo.periodo_academico_id != periodo_id:
        raise HTTPException(
            status_code=400,
            detail=(
                "El grupo no pertenece al periodo "
                "académico seleccionado"
            )
        )

    # --------------------------------------------------------
    # Evitar duplicado activo
    # --------------------------------------------------------

    activo = cambios.get(
        "activo",
        inscripcion.activo
    )

    if activo:

        existente = (
            db.query(Inscripcion)
            .filter(
                Inscripcion.usuario_id
                == inscripcion.usuario_id,

                Inscripcion.periodo_academico_id
                == periodo_id,

                Inscripcion.activo == True,

                Inscripcion.id
                != inscripcion_id
            )
            .first()
        )

        if existente:
            raise HTTPException(
                status_code=400,
                detail=(
                    "El estudiante ya tiene otra "
                    "inscripción activa en este periodo"
                )
            )

    # --------------------------------------------------------
    # Aplicar cambios
    # --------------------------------------------------------

    for campo, valor in cambios.items():
        setattr(
            inscripcion,
            campo,
            valor
        )

    db.commit()
    db.refresh(inscripcion)

    return inscripcion


# ============================================================
# CANCELAR / DESACTIVAR
# ============================================================

@router.delete(
    "/{inscripcion_id}"
)
def eliminar_inscripcion(
    inscripcion_id: int,
    db: Session = Depends(get_db),
    user=Depends(
        require_roles(
            "ADMINISTRADOR",
            "COORDINADOR_ACADEMICO"
        )
    )
):

    inscripcion = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.id == inscripcion_id
        )
        .first()
    )

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    inscripcion.activo = False

    db.commit()

    return {
        "message": "Inscripción desactivada correctamente"
    }