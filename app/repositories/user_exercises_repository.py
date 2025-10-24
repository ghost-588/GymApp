from typing import List
from datetime import date, datetime
from fastapi import Depends
from sqlalchemy.orm import Session

from app import database
from app.exceptions.exceptions import AlreadyExistsError, NotFoundError
from app.repositories.all_exercises_repository import AllExerciseRepository
from app.schemas.user_exercises_schemas import UserExerciseOut
from app.models.exercises_model import Exercise


class UserExerciseRepository:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db


    def get_all(self) -> List[UserExerciseOut]:
        exercises = self.db.query(Exercise).all()
        return exercises
    def get_all_id(self,id:int)->List[UserExerciseOut]:
        exercises = self.db.query(Exercise).filter(Exercise.user_id==id).all()
        return exercises

    def get_by_id(self, id: int) -> UserExerciseOut:
        exercise = self.db.query(Exercise).filter(Exercise.id == id).first()
        if not exercise:
            raise NotFoundError("Exercise not found")
        return exercise

    def get_by_date(self, date: datetime) -> List[UserExerciseOut]:
        exercises = self.db.query(Exercise).filter(Exercise.date == date).all()
        return exercises

    def create(self, exercise_data: dict) -> UserExerciseOut:
        existing = (
            self.db.query(Exercise)
            .filter(
                Exercise.exercise_id == exercise_data.get("exercise_id"),
                Exercise.date == date.today(),
            )
            .first()
        )
        all_exercises_repo = AllExerciseRepository(self.db)
        all_exercises_repo.get_by_id(exercise_data.get("exercise_id"))

        exercise = Exercise(**exercise_data)
        self.db.add(exercise)
        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def update(self, exercise_id: int, exercise_updates: dict) -> UserExerciseOut:
        exercise = self.get_by_id(exercise_id)

        if (
            "exercise_id" in exercise_updates
            and exercise_updates["exercise_id"] is not None
        ):
            existing = (
                self.db.query(Exercise)
                .filter(
                    Exercise.exercise_id == exercise_updates.get("exercise_id"),
                    Exercise.date == date.today(),
                )
                .first()
            )
            if existing:
                raise AlreadyExistsError("You add this exercise today")
            all_exercises_repo = AllExerciseRepository(self.db)
            all_exercises_repo.get_by_id(exercise_updates.get("exercise_id"))

        for key, value in exercise_updates.items():
            if value is not None:
                setattr(exercise, key, value)

        self.db.commit()
        self.db.refresh(exercise)
        return exercise

    def delete(self, exercise_id: int):
        exercise = self.get_by_id(exercise_id)
        self.db.delete(exercise)
        self.db.commit()
        return {"detail": "Exercise deleted successfully"}

