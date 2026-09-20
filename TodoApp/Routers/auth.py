from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from jose import jwt

from container import users_repository
from Requests.Auth.loginRequest import LoginRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'de4c91674143dfc54163c0f54774809cff3e4eb7b25b838d65f67adcf66f6fe1'
ALGORITHM = 'HS256'
EXPIRES_IN = 60 * 60 * 24

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

    # enconding for kwt token
    encode = { 'sub': username, 'id': user.id }
    expires = datetime.now() + timedelta(seconds=EXPIRES_IN)
    encode.update({'exp': expires})
    access_token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return { 'access_token': access_token, 'refresh_token': '' }