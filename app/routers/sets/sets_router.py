from typing import List
from fastapi import APIRouter, Depends

from app.exceptions.exceptions import NotAuthorizedError
from app.models.users_model import User, UserRole
from app.repositories.user_exercises_repository import UserExerciseRepository
from app.repositories.users_repositories import UserRepository
from app.schemas.sets_schemas import SetCreate, SetOut, SetUpdate
from app.repositories.sets_repository import SetRepository
from app.routers.auth.auth_router import get_current_user

router = APIRouter(prefix="/sets", tags=["Sets"])


@router.get("", response_model=List[SetOut])
def get_all_sets(
    repo: SetRepository = Depends(), 
    current_user: User = Depends(get_current_user)
):
    # FIX: Allow users to get their own sets
    if current_user.role == UserRole.ADMIN:
        sets = repo.get_all()
    else:
        sets = repo.get_by_user_id(current_user.id)  # You'll need to implement this method
    return sets


@router.get("/{set_id}", response_model=SetOut)
def get_set_by_id(
    set_id: int,
    repo: SetRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    set = repo.get_by_id(set_id)
    if current_user.role != UserRole.ADMIN and current_user.id != set.exercise.user.id:  # FIX: typo excerise -> exercise
        raise NotAuthorizedError("Not authorized")
    return set


@router.get("/exercise_id/{exercise_id}", response_model=List[SetOut])
def get_sets_by_exercise_id(
    exercise_id: int,
    repo: SetRepository = Depends(),
    exercise_repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    exercise = exercise_repo.get_by_id(exercise_id)
    if current_user.role != UserRole.ADMIN and current_user.id != exercise.user.id:
        raise NotAuthorizedError("Not authorized")
    sets = repo.get_by_exercise_id(exercise_id)
    return sets


@router.get("/user_id/{user_id}", response_model=List[SetOut])
def get_sets_by_user_id(
    user_id: int,
    repo: SetRepository = Depends(),
    user_repo: UserRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    user = user_repo.get_by_id(user_id)
    if current_user.role != UserRole.ADMIN and current_user.id != user.id:
        raise NotAuthorizedError("Not authorized")
    sets = repo.get_by_user_id(user_id)
    return sets


@router.post("", response_model=SetOut)
def create_set(
    set_data: SetCreate,
    repo: SetRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    return repo.create(set_data.model_dump())


@router.put("/{set_id}", response_model=SetOut)
def update_set(
    set_id: int,
    set_updates: SetUpdate,
    repo: SetRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    return repo.update(set_id, set_updates.model_dump())


@router.delete("/{set_id}")
def delete_set(
    set_id: int,
    repo: SetRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    return repo.delete(set_id)