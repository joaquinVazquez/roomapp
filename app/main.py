from fastapi import FastAPI
from app.db.connection import engine
from app.db.base import Base
from app import models
from app.routes import auth
from app.routes import users
from app.routes import programas

app = FastAPI()


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(programas.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}