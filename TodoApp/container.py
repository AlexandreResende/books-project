from typing import Annotated
from fastapi import Depends

from Repository.todosRepository import TodosRepository
from Repository.usersRepository import UsersRepository

# repository
todos_repository = Annotated[TodosRepository, Depends(TodosRepository)]
users_repository = Annotated[UsersRepository, Depends(UsersRepository)]