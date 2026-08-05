from fastapi import FastAPI

import models
from TodoApp.database import SessionLocal
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/healthz")
def health_check():
    return { "message": "Ok"}

@app.get("/todos")
def get_todos():
    pass