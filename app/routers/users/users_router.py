from typing import List
from fastapi import APIRouter, Depends

from app.exceptions.exceptions import NotAuthorizedError
from app.models.users_model import User, UserRole
from app.routers.auth.auth_router import get_current_user
from app.schemas.users_schemas import UserCreate, UserOut, UserUpdate
from app.repositories.users_repositories import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def get_all_users(
    repo: UserRepository = Depends(), current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.ADMIN:
        raise NotAuthorizedError("Not authorized")
    return repo.get_all()


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(
    user_id: int,
    repo: UserRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise NotAuthorizedError("Not authorized")
    return repo.get_by_id(user_id)


@router.get("/role/{user_id}", response_model=UserRole)
def get_user_role(
    user_id: int,
    repo: UserRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise NotAuthorizedError("Not authorized")
    return repo.get_user_role(user_id)


@router.post("/", response_model=UserOut)
def create_user(user_data: UserCreate, repo: UserRepository = Depends()):
    return repo.create(user_data.model_dump())


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_updates: UserUpdate,
    repo: UserRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise NotAuthorizedError("Not authorized")
    return repo.update(user_id, user_updates.model_dump())


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    repo: UserRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN and current_user.id != user_id:
        raise NotAuthorizedError("Not authorized")
    return repo.delete(user_id)
