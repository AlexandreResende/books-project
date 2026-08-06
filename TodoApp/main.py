from fastapi import FastAPI, Depends, status
from typing import Annotated
from sqlalchemy.orm import Session

import models
from models import Todos
from database import engine, SessionLocal
from Requests.createTodoRequest import CreateTodoRequest
from Entities.todoEntity import TodoEntity

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/healthz")
def health_check():
    return { "message": "Ok"}

@app.get("/todos", status_code=status.HTTP_200_OK)
def get_all_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(Todos).all()

    return { "todos": todos }

@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(db: db_dependency, todo_request: CreateTodoRequest):
    todo = TodoEntity(**todo_request.model_dump())

    db.add(todo.to_database())
    db.commit()

    return {}