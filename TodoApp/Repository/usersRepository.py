from models import Users
from database import db_dependency

from Entities.userEntity import UserEntity

class UsersRepository():
    def __init__(self, db:db_dependency):
        self.db = db

    def create_user(self, user:UserEntity):
        self.db.add(user.to_database())
        self.db.commit()

        return