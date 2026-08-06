from fastapi import FastAPI, Depends, HTTPException, Path, status
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
async def health_check():
    return { "message": "Ok"}

@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: Annotated[Session, Depends(get_db)]):
    todos = db.query(Todos).all()

    return { "todos": todos }

@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    todoEntity = TodoEntity.from_database(**todo_model.to_json())

    return todoEntity

@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: CreateTodoRequest):
    todo = TodoEntity(**todo_request.model_dump())

    db.add(todo.to_database())
    db.commit()

    return {}