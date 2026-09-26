from fastapi import APIRouter, HTTPException, status

from Entities.userEntity import UserEntity
from container import users_repository
from Requests.Users.createUserRequest import CreateUserRequest

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