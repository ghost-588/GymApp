from typing import Optional
from pydantic import BaseModel, field_validator

from app.exceptions.exceptions import ValidationError
from app.schemas.user_exercises_schemas import UserExerciseOut


class SetCreate(BaseModel):
    reps: int
    weight: float
    exercise_id: int

    @field_validator("reps")
    def validate_reps(cls, value: int) -> int:
        if value <= 0:
            raise ValidationError("Reps must be greater than 0")
        return value

    @field_validator("weight")
    def validate_weight(cls, value: float) -> float:
        if value <= 0:
            raise ValidationError("Weight must be greater than 0")
        return value

    @field_validator("exercise_id")
    def validate_exercise_id(cls, value: int) -> int:
        if value <= 0:
            raise ValidationError("Exercise id must be greater than 0")
        return value

    model_config = {"from_attributes": True}


class SetUpdate(BaseModel):
    reps: Optional[int] = None
    weight: Optional[float] = None
    exercise_id: Optional[int] = None

    @field_validator("reps")
    def validate_reps(cls, value: int) -> int:
        if value is not None and value <= 0:
            raise ValidationError("Reps must be greater than 0")
        return value

    @field_validator("weight")
    def validate_weight(cls, value: float) -> float:
        if value is not None and value <= 0:
            raise ValidationError("Weight must be greater than 0")
        return value

    @field_validator("exercise_id")
    def validate_exercise_id(cls, value: int) -> int:
        if value is not None and value <= 0:
            raise ValidationError("Exercise id must be greater than 0")
        return value

    model_config = {"from_attributes": True}


class SetOut(BaseModel):
    reps: int
    weight: float
    exercise: UserExerciseOut
