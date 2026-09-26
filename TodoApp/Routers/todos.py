from fastapi import APIRouter, HTTPException, Path, status

from Requests.createTodoRequest import CreateTodoRequest
from Requests.updateTodoRequest import UpdateTodoRequest
from Entities.todoEntity import TodoEntity
from container import todos_repository, user_dependency

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)

@router.get("/healthz")
async def health_check():
    return { "message": "Ok"}

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_todos(user: user_dependency, repository: todos_repository):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail ="Authentication failed")

    todos = repository.get_all_todos(user.get('id'))

    return { "todos": todos }

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(user: user_dependency, repository: todos_repository, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    record = repository.get_todo_by_id(todo_id)

    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if record.owner_id != user.get('id'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return record

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, repository: todos_repository, todo_request: CreateTodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    repository.create_todo(TodoEntity(**todo_request.model_dump(), owner_id=user.get('id')))

    return {}

@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, repository: todos_repository, updated_todo_request: UpdateTodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    record = repository.get_todo_by_id(todo_id)

    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    if record.owner_id != user.get('id'):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    record.update_todo(**updated_todo_request.model_dump())

    repository.update_todo(record)

    return

@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user: user_dependency, repository: todos_repository, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    result = repository.delete_todo(todo_id, user.get('id'))

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")

    return { "message": "Record deleted" }