from database import  Base

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

    def __init__(self, email, username, first_name, last_name, password, is_active, roles, id=None):
        self.id = id
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_active = is_active
        self.roles = roles

        def to_json(self):
            return {
                "id": self.id,
                "email": self.email,
                "username": self.username,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "is_active": self.is_active,
                "roles": self.roles,
                "password": self.password
            }

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('Users.id'))

    def __init__(self, title, priority, owner_id, completed=False, description=None, id=None):
        self.title = title
        self.priority = priority
        self.completed = completed
        self.description = description
        self.id = id
        self.owner_id = owner_id

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "owner_id": self.owner_id
        }