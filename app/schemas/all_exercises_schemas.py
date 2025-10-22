from typing import Optional
from pydantic import BaseModel, Field


class AllExercisesCreate(BaseModel):
    name: str = Field(min_length=3)
    url: str = Field(min_length=3)
    description: str = Field(min_length=3)

    model_config = {"from_attributes": True}


class AllExercisesUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None

    model_config = {"from_attributes": True}


class AllExercisesOut(BaseModel):
    id: int
    name: str
    url: str
    description: str
