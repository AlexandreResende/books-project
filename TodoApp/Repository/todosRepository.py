from models import Todos
from database import db_dependency

class TodosRepository:
    def __init__(self, db: db_dependency):
        self.db = db

    def delete_todo(self, todo_id: int):
        rows_deleted = self.db.query(Todos).filter(Todos.id == todo_id).delete(synchronize_session=False)
        self.db.commit()

        if rows_deleted == 0:
            return None

        return True