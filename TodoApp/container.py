from typing import Annotated
from fastapi import Depends

from Repository.todosRepository import TodosRepository

# repository
todos_repository = Annotated[TodosRepository, Depends(TodosRepository)]