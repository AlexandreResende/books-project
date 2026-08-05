from fastapi import FastAPI, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session

import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/healthz")
def health_check():
    return { "message": "Ok"}

@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(Todos).all()

    return { "todos": todos }