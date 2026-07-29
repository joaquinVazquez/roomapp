from fastapi import FastAPI
from app.db.connection import engine
from app.db.base import Base
from app import models
from app.routes import auth
from app.routes import users
from app.routes import programas
from app.routes import materias
from app.routes import programa_materias
from app.routes import aulas
from app.routes import horarios
from app.routes import periodo_academico
from app.routes import actividades_academicas
from app.routes import grupo
from app.routes import notificaciones

app = FastAPI()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(programas.router)
app.include_router(materias.router)
app.include_router(programa_materias.router)
app.include_router(aulas.router)
app.include_router(horarios.router)
app.include_router(periodo_academico.router)
app.include_router(actividades_academicas.router)
app.include_router(grupo.router)
app.include_router(notificaciones.router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}