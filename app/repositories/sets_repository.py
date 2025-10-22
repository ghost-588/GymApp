from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app import database
from app.exceptions.exceptions import NotFoundError
from app.models.exercises_model import Exercise
from app.models.sets_model import Set
from app.repositories.user_exercises_repository import UserExerciseRepository
from app.schemas.sets_schemas import SetOut


class SetRepository:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def get_all(self) -> List[SetOut]:
        sets = self.db.query(Set).all()
        return sets

    def get_by_id(self, set_id: int) -> SetOut:
        set = self.db.query(Set).filter(Set.id == set_id).first()
        if not set:
            raise NotFoundError("Set not found")
        return set

    def get_by_exercise_id(self, exercise_id: int) -> SetOut:
        sets = self.db.query(Set).filter(Set.exercise_id == exercise_id).all()
        return sets

    def get_by_user_id(self, user_id: int) -> SetOut:
        sets = (
            self.db.query(Set)
            .join(Exercise, Set.exercise_id == Exercise.id)
            .filter(Exercise.user_id == user_id)
            .all()
        )
        return sets

    def create(self, set_data: dict) -> SetOut:
        exercise_repo = UserExerciseRepository(self.db)
        exercise_repo.get_by_id(set_data["exercise_id"])

        set = Set(**set_data)
        self.db.add(set)
        self.db.commit()
        self.db.refresh(set)
        return set

    def update(self, set_id: int, set_updates: dict) -> SetOut:
        set = self.get_by_id(set_id)

        if "exercise_id" in set_updates:
            exercise_repo = UserExerciseRepository(self.db)
            exercise_repo.get_by_id(set_updates["id"])

        for key, value in set_updates.items():
            if value is not None:
                setattr(set, key, value)

        self.db.commit()
        self.db.refresh(set)
        return set

    def delete(self, set_id):
        set = self.get_by_id(set_id)
        self.db.delete(set)
        self.db.commit()
        return {"detial": "Set deleted succesfully"}
