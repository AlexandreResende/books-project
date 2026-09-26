from typing import Optional

from models import Todos

class TodoEntity():
    id: Optional[int]
    title: str
    description: Optional[str]
    priority: int
    completed: bool
    owner_id: int

    def __init__(self, title, priority, owner_id, id = None, description = None, completed = False):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed
        self.owner_id = owner_id

    def to_database(self):
        return Todos(
            title=self.title,
            priority=self.priority,
            owner_id=self.owner_id,
            completed=self.completed,
            description=self.description,
            id=self.id
        )

    def update_todo(self, title, description, priority, completed):
        self.title = title if title is not None else self.title
        self.description = description if description is not None else self.description
        self.priority = priority if priority is not None else self.priority
        self.completed = completed if completed is not None else self.completed

    @staticmethod
    def from_database(id, title, description, priority, completed, owner_id):
        return TodoEntity(
            id=id,
            title=title,
            description=description,
            priority=priority,
            completed=completed,
            owner_id=owner_id
        )