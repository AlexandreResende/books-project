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

    def get_users(self):
        users = self.db.query(Users).all()

        return [UserEntity.from_database(**user.to_json()) for user in users]