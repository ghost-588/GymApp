from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends

from app.exceptions.exceptions import NotFoundError
from app.models.all_exercises_model import AllExercises
from app import database
from app.schemas.all_exercises_schemas import AllExercisesOut


class AllExerciseRepository:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def get_all(self) -> List[AllExercisesOut]:
        exercises = self.db.query(AllExercises).all()
        return exercises

    def get_by_id(self, exercise: int) -> List[AllExercisesOut]:
        exercise = (
            self.db.query(AllExercises).filter(AllExercises.id == exercise).first()
        )
        if not exercise:
            raise NotFoundError("Exercise not found")
        return exercise

    def get_by_name(self, exercise_name: str) -> List[AllExercisesOut]:
        exercise = (
            self.db.query(AllExercises)
            .filter(AllExercises.name == exercise_name)
            .first()
        )
        if not exercise:
            raise NotFoundError("Exercise not found")
        return exercise

    def create(self, exercise_data: dict) -> AllExercisesOut:
        exercise = AllExercises(**exercise_data)
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def update(self, id: int, exercise_updates: dict) -> AllExercisesOut:
        exercise = self.get_by_id(id)
        for key, value in exercise_updates.items():
            if value is not None:
                setattr(exercise, key, value)
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def delete(self, id: int):
        exercise = self.get_by_id(id)
        self.db.delete(exercise)
        self.db.commit()
        return {"detail": "Exercise deleted successfully"}
