from typing import List

from fastapi import APIRouter, Depends

from app.exceptions.exceptions import NotAuthorizedError
from app.models.users_model import User, UserRole
from app.repositories.all_exercises_repository import AllExerciseRepository
from app.routers.auth.auth_router import get_current_user
from app.schemas.all_exercises_schemas import (
    AllExercisesCreate,
    AllExercisesOut,
    AllExercisesUpdate,
)

router = APIRouter(prefix="/all_exercises", tags=["AllExercises"])


@router.get("/", response_model=List[AllExercisesOut])
async def get_all_exercises(
    repo: AllExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    return repo.get_all()


@router.get("/{exercise_id}", response_model=AllExercisesOut)
async def get_exercises_by_id(
    exercise_id: int,
    repo: AllExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    exercise = repo.get_by_id(exercise_id)
    return exercise


@router.get("/name/{exercise_name}", response_model=AllExercisesOut)
async def get_exercises_by_name(
    exercise_name: str,
    repo: AllExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    exercise = repo.get_by_name(exercise_name)
    return exercise


@router.post("/")
async def create_exercise(
    exercise_data: AllExercisesCreate,
    repo: AllExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise NotAuthorizedError("Not authorized")
    return repo.create(exercise_data.model_dump())


@router.put("/{exercise_id}")
async def exercise_update(
    exercise_id: int,
    exercise_updates: AllExercisesUpdate,
    repo: AllExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise NotAuthorizedError("Not authorized")
    return repo.update(exercise_id, exercise_updates.model_dump())


@router.delete("/{exercise_id}")
async def delete_exercise(
    exercise_id: int,
    repo: AllExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.ADMIN:
        raise NotAuthorizedError("Not authorized")
    return repo.delete(exercise_id)
