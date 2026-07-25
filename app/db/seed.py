from sqlalchemy.orm import Session
from app.models.rol import Rol
from app.models.dia_semana import DiaSemana

def seed_dias_semana(db: Session):

    dias = [
        {
            "nombre": "Lunes",
            "abreviatura": "LUN",
            "numero": 1
        },
        {
            "nombre": "Martes",
            "abreviatura": "MAR",
            "numero": 2
        },
        {
            "nombre": "Miércoles",
            "abreviatura": "MIE",
            "numero": 3
        },
        {
            "nombre": "Jueves",
            "abreviatura": "JUE",
            "numero": 4
        },
        {
            "nombre": "Viernes",
            "abreviatura": "VIE",
            "numero": 5
        },
        {
            "nombre": "Sábado",
            "abreviatura": "SAB",
            "numero": 6
        },
        {
            "nombre": "Domingo",
            "abreviatura": "DOM",
            "numero": 7
        },
    ]

    for dia in dias:

        existe = db.query(DiaSemana).filter(
            DiaSemana.numero == dia["numero"]
        ).first()

        if not existe:
            nuevo_dia = DiaSemana(
                nombre=dia["nombre"],
                abreviatura=dia["abreviatura"],
                numero=dia["numero"]
            )

            db.add(nuevo_dia)

    db.commit()


def seed_roles(db: Session):
    roles = [
        "ADMINISTRADOR",
        "COORDINADOR_ACADEMICO",
        "DOCENTE",
        "ESTUDIANTE",
        "PERSONAL_ADMINISTRATIVO",
    ]

    for rol_nombre in roles:
        existe = db.query(Rol).filter(Rol.nombre == rol_nombre).first()
        if not existe:
            nuevo_rol = Rol(nombre=rol_nombre)
            db.add(nuevo_rol)

    db.commit()