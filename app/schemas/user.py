from pydantic import BaseModel, EmailStr


# Datos para crear usuario
class UserCreate(BaseModel):

    nombre: str
    apellido: str

    email: EmailStr

    password: str

    rol_id: int


# Datos para login
class UserLogin(BaseModel):

    email: EmailStr
    password: str


# Respuesta de usuario
class UserResponse(BaseModel):

    id: int

    nombre: str
    apellido: str

    email: EmailStr

    rol_id: int

    activo: bool


    class Config:
        from_attributes = True