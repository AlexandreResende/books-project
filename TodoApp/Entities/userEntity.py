from typing import Optional
from passlib.context import CryptContext

from models import Users

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserEntity():
    id: Optional[int]
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    roles: str

    def __init__(self, username: str, email: str,first_name: str, last_name: str, password: str, is_active: bool, roles: str, id = None):
        self.id = id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = bcrypt_context.hash(password)
        self.is_active = is_active
        self.roles = roles

    def to_database(self):
        return Users(
            id = self.id,
            username = self.username,
            email = self.email,
            first_name = self.first_name,
            last_name = self.last_name,
            hashed_password = self.password,
            is_active = self.is_active,
            roles = self.roles
        )

    @staticmethod
    def from_database(id: int, username: str, email: str, first_name: str, last_name: str, hashed_password: str, is_active: bool, roles: str):
        user = UserEntity(username, email, first_name, last_name, '', is_active, roles, id)
        user.password = hashed_password

        return user

    def update_password(self, password: str):
        self.password = bcrypt_context.hash(password)