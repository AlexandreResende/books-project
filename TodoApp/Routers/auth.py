from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError

from container import users_repository
from Requests.Auth.loginRequest import LoginRequest

router = APIRouter()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'de4c91674143dfc54163c0f54774809cff3e4eb7b25b838d65f67adcf66f6fe1'
ALGORITHM = 'HS256'
EXPIRES_IN = 60 * 60 * 24

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

        return {
            'username': username,
            'id': user_id
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

@router.get("/auth/")
async def get_user():
    return { "user": "authenticated" }

@router.post('/login')
async def login(repository: users_repository, request: LoginRequest):
    username = request.username
    password = request.password

    user = repository.get_user_by_username(username)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

    if bcrypt_context.verify(password, user.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid username or password')

    # enconding for kwt token
    encode = { 'sub': username, 'id': user.id }
    expires = datetime.now() + timedelta(seconds=EXPIRES_IN)
    encode.update({'exp': expires})
    access_token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return { 'access_token': access_token, 'refresh_token': '' }