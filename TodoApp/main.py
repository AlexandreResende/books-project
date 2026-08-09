from fastapi import FastAPI, HTTPException, Path, status

import models
from database import engine
from Requests.createTodoRequest import CreateTodoRequest
from Requests.updateTodoRequest import UpdateTodoRequest
from Entities.todoEntity import TodoEntity
from container import todos_repository

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/healthz")
async def health_check():
    return { "message": "Ok"}

@app.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(repository: todos_repository):
    todos = repository.get_all_todos()

    return { "todos": todos }

@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(repository: todos_repository, todo_id: int = Path(gt=0)):
    record = repository.get_todo_by_id(todo_id)

    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    return record

@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(repository: todos_repository, todo_request: CreateTodoRequest):
    repository.create_todo(TodoEntity(**todo_request.model_dump()))

    return {}

@app.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(repository: todos_repository, updated_todo_request: UpdateTodoRequest, todo_id: int = Path(gt=0)):
    todo_new_data = updated_todo_request.model_dump()
    result = repository.update_todo(todo_id, todo_new_data)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    return

@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(repository: todos_repository, todo_id: int = Path(gt=0)):
    result = repository.delete_todo(todo_id)

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return { "message": "Record deleted" }