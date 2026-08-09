from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends

from TodoApp.Repository.todosRepository import TodosRepository
from TodoApp.database import get_db

#database
db_dependency = Annotated[Session, Depends(get_db())]
