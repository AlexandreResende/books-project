from typing import Annotated
from fastapi import Depends

from Auth.authService import get_current_user

from Repository.todosRepository import TodosRepository
from Repository.usersRepository import UsersRepository

# repository
todos_repository = Annotated[TodosRepository, Depends(TodosRepository)]
users_repository = Annotated[UsersRepository, Depends(UsersRepository)]

# auth middleware
user_dependency = Annotated[dict, Depends(get_current_user)]