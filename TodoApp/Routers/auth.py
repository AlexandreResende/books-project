from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import jwt

from container import users_repository

from Auth.authService import SECRET_KEY, ALGORITHM, EXPIRES_IN

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.get("/")
async def get_user():
    return { "user": "authenticated" }

@router.post('/login')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], repository: users_repository):
    username = form_data.username
    password = form_data.password

    user = repository.get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    if bcrypt_context.verify(password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid username or password')

    # enconding for kwt token
    encode = { 'sub': username, 'id': user.id, 'roles': user.roles }
    expires = datetime.now() + timedelta(seconds=EXPIRES_IN)
    encode.update({'exp': expires})
    access_token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return { 'access_token': access_token, 'refresh_token': '' }