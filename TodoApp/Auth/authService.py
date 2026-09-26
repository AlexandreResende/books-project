from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

SECRET_KEY = 'de4c91674143dfc54163c0f54774809cff3e4eb7b25b838d65f67adcf66f6fe1'
ALGORITHM = 'HS256'
EXPIRES_IN = 60 * 60 * 24

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        roles: str = payload.get('roles')

        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')

        return {
            'username': username,
            'id': user_id,
            'roles': roles
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')