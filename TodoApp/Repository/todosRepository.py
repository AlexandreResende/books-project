from models import Todos
from database import db_dependency

from Entities.todoEntity import TodoEntity

class TodosRepository:
    def __init__(self, db: db_dependency):
        self.db = db

    def delete_todo(self, todo_id: int):
        rows_deleted = self.db.query(Todos).filter(Todos.id == todo_id).delete(synchronize_session=False)
        self.db.commit()

        if rows_deleted == 0:
            return None

        return True

    def get_todo_by_id(self, todo_id: int):
        todo_model = self.db.query(Todos).filter(Todos.id == todo_id).first()

        if todo_model is None:
            return None

        return TodoEntity.from_database(**todo_model.to_json())

    def get_all_todos(self):
        todos_model = self.db.query(Todos).all()

        return [TodoEntity.from_database(**todo_model.to_json()) for todo_model in todos_model]

    def create_todo(self, todo: TodoEntity):
        self.db.add(todo.to_database())
        self.db.commit()

        return