from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext

from container import users_repository
from Requests.Auth.loginRequest import LoginRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get("/auth/")
async def get_user():
    return { "user": "authenticated" }

@router.post('/login')
async def login(repository: users_repository, request: LoginRequest):
    username = request.username
    password = request.password

    user = repository.get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    if bcrypt_context.verify(password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid username or password')

    return { 'access_token': '', 'refresh_token': '' }