from typing import Optional

from models import Todos

class TodoEntity():
    id: Optional[int]
    title: str
    description: Optional[str]
    priority: int
    completed: bool

    def __init__(self, title, priority, id = None, description = None, completed = False):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed

    def to_database(self):
        return Todos(
            self.title,
            self.priority,
            self.completed,
            self.description
        )

    def from_database(self):
        pass