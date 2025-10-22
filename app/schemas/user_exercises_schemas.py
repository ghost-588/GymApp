from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.all_exercises_schemas import AllExercisesOut
from app.schemas.users_schemas import UserOut


class UserExerciseCreate(BaseModel):
    exercise_id: int

    model_config = {"from_attributes": True}


class UserExerciseUpdate(BaseModel):
    exercise_id: Optional[int] = None

    model_config = {"from_attributes": True}


class UserExerciseOut(BaseModel):
    id: int
    date: datetime
    exercise: AllExercisesOut
    user: UserOut
