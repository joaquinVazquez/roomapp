from app.db.session import SessionLocal
from app.models.persona import Persona
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.usuario_rol import UsuarioRol
from app.core.security import hash_password


def run():
    db = SessionLocal()

    try:
        # 1. Verificar si ya existe
        existe = db.query(Usuario).filter(Usuario.email == "admin@roomapp.com").first()
        if existe:
            print("El usuario ya existe")
            return

        # 2. Crear persona
        persona = Persona(
            nombres="Joaquin",
            apellido_paterno="Vazquez"
        )
        db.add(persona)
        db.commit()
        db.refresh(persona)

        # 3. Crear usuario
        usuario = Usuario(
            persona_id=persona.id,
            email="admin@roomapp.com",
            password_hash=hash_password("123456")
        )
        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        # 4. Obtener rol ADMINISTRADOR
        rol_admin = db.query(Rol).filter(Rol.nombre == "ADMINISTRADOR").first()

        # 5. Asignar rol
        usuario_rol = UsuarioRol(
            usuario_id=usuario.id,
            rol_id=rol_admin.id
        )
        db.add(usuario_rol)
        db.commit()

        print("Usuario administrador creado correctamente")

    finally:
        db.close()


if __name__ == "__main__":
    run()