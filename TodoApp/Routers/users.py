from fastapi import APIRouter, HTTPException, status

from Entities.userEntity import UserEntity
from container import users_repository, user_dependency
from Requests.Users.createUserRequest import CreateUserRequest
from Requests.Users.updatePasswordRequest import UpdatePasswordRequest

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(repository: users_repository, request: CreateUserRequest):
    if request.roles == 'admin' and request.email != 'a@gmail.com':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Admin role not allowed')
    repository.create_user(UserEntity(**request.model_dump()))

    return {}

@router.get('/', status_code=status.HTTP_200_OK)
async def get_users(repository: users_repository):
    users = repository.get_users()

    return { 'users': users }

@router.get('/{user_id}')
async def get_user_by_id(repository: users_repository, user_id: int):
    user = repository.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    return user

@router.put('/password', status_code=status.HTTP_200_OK)
async def update_password(user: user_dependency, repository: users_repository, update_password_request: UpdatePasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')

    user_entity = repository.get_user_by_id(user.get('id'))

    if user_entity is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

    user_entity.update_password(update_password_request.password)

    repository.update_user(user_entity)

    return {}