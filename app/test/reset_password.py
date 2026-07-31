from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.usuario import Usuario


db = SessionLocal()


usuario = (
    db.query(Usuario)
    .filter(
        Usuario.email == "docente.prueba@unisa.edu.mx"
    )
    .first()
)


if usuario:

    usuario.password_hash = hash_password("123456")

    db.commit()

    print("Contraseña actualizada correctamente")

else:

    print("Usuario no encontrado")


db.close()