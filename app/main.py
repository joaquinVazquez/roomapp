from fastapi import FastAPI
from app.db.connection import engine
from app.db.base import Base
from app import models
from app.routes import user

app = FastAPI()


app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}