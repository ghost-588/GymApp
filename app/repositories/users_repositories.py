from typing import List
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from fastapi import Depends

from app import database
from app.models.users_model import User, UserRole
from app.schemas.users_schemas import UserOut
from app.exceptions.exceptions import NotFoundError, AlreadyExistsError


class UserRepository:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def get_all(self) -> List[UserOut]:
        users = self.db.query(User).all()
        return users

    def get_by_id(self, user_id: int) -> UserOut:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundError("User not found")
        return user

    def get_by_email(self, email: str) -> UserOut:
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise NotFoundError("User not found")
        return user

    def get_user_role(self, user_id: int) -> UserRole:
        user = self.get_by_id(user_id)
        return user.role

    def create(self, user_data: dict) -> UserOut:
        # Check if email exists
        existing = (
            self.db.query(User).filter(User.email == user_data.get("email")).first()
        )
        if existing:
            raise AlreadyExistsError("User with this email already exists")

        hashed_password = bcrypt.hash(user_data.pop("password"))
        user_data["hashed_password"] = hashed_password

        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user_id: int, updates: dict) -> UserOut:
        user = self.get_by_id(user_id)

        if "email" in updates and updates["email"] is not None:
            existing = (
                self.db.query(User).filter(User.email == updates.get("email")).first()
            )
            if existing and existing.id != user_id:
                raise AlreadyExistsError("User with this email already exists")

        password = updates.pop("password", None)
        if password:
            updates["hashed_password"] = bcrypt.hash(password)

        for key, value in updates.items():
            if value is not None:
                setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int):
        user = self.get_by_id(user_id)
        self.db.delete(user)
        self.db.commit()
        return {"detail": "User deleted successfully"}
