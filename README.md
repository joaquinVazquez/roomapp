# RoomApp

Sistema de Gestión de Horarios y Espacios Académicos

## Descripción

RoomApp es una aplicación web orientada a instituciones educativas para gestionar:

- Horarios académicos
- Asignación de aulas y espacios
- Usuarios con roles
- Consulta de información académica

El objetivo es desarrollar un MVP reutilizable para diferentes instituciones.

---

# Estado del proyecto

## Fase actual

Fase 2 - Gestión de usuarios y permisos


## Funcionalidades implementadas

### Autenticación

✅ Login mediante correo y contraseña

✅ Generación de tokens JWT

✅ Protección de endpoints mediante autenticación


### Usuarios

✅ Creación de usuarios

✅ Asociación Persona - Usuario

✅ Asignación de rol

✅ Activación/desactivación de cuentas


### Roles

Roles definidos:

- ADMINISTRADOR
- COORDINADOR_ACADEMICO
- DOCENTE
- ESTUDIANTE
- PERSONAL_ADMINISTRATIVO


---

# Arquitectura actual

## Modelo de usuarios


Persona

```
id
nombre
apellido
email
created_at
```


Usuario

```
id
persona_id
rol_id
email
password_hash
activo
ultimo_acceso
created_at
```


Rol

```
id
nombre
descripcion
activo
```


Relaciones:

```
Persona 1 ---- 1 Usuario

Usuario N ---- 1 Rol
```


---

# Tecnologías utilizadas

## Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic


## Seguridad

- JWT
- Passlib
- Bcrypt


## Herramientas

- Git
- GitHub
- Visual Studio Code


---

# Estructura actual


```
roomapp/

app/

 ├── core/
 │    └── security.py
 │
 ├── db/
 │    ├── base.py
 │    ├── base_class.py
 │    └── session.py
 │
 ├── models/
 │    ├── persona.py
 │    ├── usuario.py
 │    └── rol.py
 │
 ├── routes/
 │    └── user.py
 │
 └── schemas/


alembic/

create_admin.py

README.md

```

---

# Seguridad

Actualmente implementado:

- Hash de contraseñas con bcrypt
- Tokens JWT
- Validación de roles
- Protección de rutas privadas


Ejemplo:

```
GET /admin-only
```

requiere:

```
ADMINISTRADOR
```


---

# Base de datos

Motor:

PostgreSQL


Tablas principales:

- personas
- usuarios
- roles


Tabla antigua pendiente:

- usuario_roles

Actualmente no participa en la lógica del sistema.


---

# Próximas funcionalidades

## Administración de usuarios

Pendiente:

- Listar usuarios
- Consultar usuario
- Activar/desactivar usuarios
- Cambiar rol


## Próximos módulos

- Gestión de aulas
- Gestión de materias
- Gestión de grupos
- Gestión de horarios
- Asignación de espacios


---

# Decisiones importantes

## Roles

Se decidió utilizar:

```
Usuario -> Rol
```

Un usuario solamente tiene un rol activo.


## Historial

Se conservará información para futuras auditorías.


---

# Ejecución local


Activar entorno:

```
venv\Scripts\activate
```


Ejecutar API:

```
python -m uvicorn app.main:app --reload
```


Swagger:

```
http://127.0.0.1:8000/docs
```
