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

    def get_user_by_username(self, username: str):
        user = self.db.query(Users).filter(Users.username == username).first()

        if not user:
            return None

        return UserEntity.from_database(**user.to_json())

    def get_user_by_id(self, user_id: int):
        user = self.db.query(Users).filter(Users.id == user_id).first()

        if not user:
            return None

        return UserEntity.from_database(**user.to_json())