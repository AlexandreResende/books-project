from fastapi import HTTPException, APIRouter, status, Path

from container import todos_repository, user_dependency

router = APIRouter(
    prefix='/admin',
    tags=['admin'],
)

# It will be interesting to have admin endpoints to handle
# user operations

@router.get('/todos')
async def get_todos(user: user_dependency, repository: todos_repository):
    print(user.get('roles'))
    if user is None or user.get('roles') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    todos = repository.get_all_todos_admin()

    return { 'todos': todos }

@router.get('/todos/{todo_id}')
async def get_todo(user: user_dependency, repository: todos_repository, todo_id: int):
    if user is None or user.get('roles') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    todo = repository.get_todo_by_id(todo_id)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

    return todo

@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, repository: todos_repository, todo_id: int):
    if user is None or user.get('roles') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    repository.delete_todo_admin(todo_id)

    return {}