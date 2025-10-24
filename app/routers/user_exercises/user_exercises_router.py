from datetime import date, datetime
from typing import List
from fastapi import APIRouter, Depends

from app.exceptions.exceptions import NotAuthorizedError
from app.models.users_model import User, UserRole
from app.repositories.user_exercises_repository import UserExerciseRepository
from app.routers.auth.auth_router import get_current_user
from app.schemas.user_exercises_schemas import (
    UserExerciseCreate,
    UserExerciseOut,
    UserExerciseUpdate,
)

router = APIRouter(prefix="/user_exercises", tags=["UserExercises"])


@router.get("", response_model=List[UserExerciseOut])
def get_all_user_exercises(
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    # FIX: Allow users to get their own exercises
    if current_user.role == UserRole.ADMIN:
        return repo.get_all()
    else:
        return repo.get_all_id(current_user.id)  # You'll need to implement this method

@router.get("/user", response_model=List[UserExerciseOut])
def get_all_user_exercise(
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):

    return repo.get_all_id(current_user.id)  # You'll need to implement this method

@router.get("/{exercise_id}", response_model=UserExerciseOut)
def get_user_exercise_by_id(
    exercise_id: int,
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    exercise = repo.get_by_id(exercise_id)
    if current_user.role != UserRole.ADMIN and current_user.id != exercise.user.id:
        raise NotAuthorizedError("Not authorized")
    return exercise


@router.get("/date/{date}", response_model=List[UserExerciseOut])  # FIX: Changed path to avoid conflict
def get_user_exercise_by_date(
    date: date,  # FIX: Changed from datetime to date
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    # FIX: Allow users to get their own exercises by date
    if current_user.role == UserRole.ADMIN:
        exercises = repo.get_by_date(date)
    else:
        exercises = repo.get_by_user_id_and_date(current_user.id, date)  # You'll need to implement this
    return exercises


@router.post("", response_model=UserExerciseOut)
def create_user_exercise(
    user_exercise_data: UserExerciseCreate,
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    data = user_exercise_data.model_dump()
    data["date"] = date.today()
    data["user_id"] = current_user.id
    return repo.create(data)


@router.put("/{exercise_id}", response_model=UserExerciseOut)
def update_user_exercise(
    exercise_id: int,
    user_exercise_updates: UserExerciseUpdate,
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    user_exercise = repo.get_by_id(exercise_id)
    if current_user.role != UserRole.ADMIN and current_user.id != user_exercise.user.id:
        raise NotAuthorizedError("Not authorized")
    return repo.update(exercise_id, user_exercise_updates.model_dump())


@router.delete("/{exercise_id}")
def delete_user_exercise(
    exercise_id: int,
    repo: UserExerciseRepository = Depends(),
    current_user: User = Depends(get_current_user),
):
    user_exercise = repo.get_by_id(exercise_id)
    if current_user.role != UserRole.ADMIN and current_user.id != user_exercise.user.id:
        raise NotAuthorizedError("Not authorized")

    return repo.delete(exercise_id)
