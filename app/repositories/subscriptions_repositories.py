from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session

from app import database
from app.exceptions.exceptions import BusinessRuleError, NotFoundError
from app.models.subscriptions_model import Subscription
from app.models.users_model import UserRole
from app.repositories.users_repositories import UserRepository
from app.schemas.subscription_schemas import SubscriptionOut


class SubscriptionRepository:
    def __init__(self, db: Session = Depends(database.get_db)):
        self.db = db

    def get_all(self) -> List[SubscriptionOut]:
        subs = self.db.query(Subscription).all()
        return subs

    def get_by_id(self, sub_id) -> SubscriptionOut:
        sub = self.db.query(Subscription).filter(Subscription.id == sub_id).first()
        if not sub:
            raise NotFoundError("Subscription not found")
        return sub

    def create(self, sub_data) -> SubscriptionOut:
        user_repo = UserRepository(self.db)
        non_admin_user = user_repo.get_by_id(sub_data["user_id"])

        if non_admin_user.role == UserRole.ADMIN:
            raise BusinessRuleError("The admin don't have subscription")

        sub = Subscription(**sub_data)
        self.db.add(sub)
        self.db.commit()
        self.db.refresh(sub)
        return sub

    def update(self, sub_id, sub_updates: dict) -> SubscriptionOut:
        sub = self.get_by_id(sub_id)

        if "user_id" in sub_updates and sub_updates["user_id"] is not None:
            user_repo = UserRepository(self.db)
            non_admin_user = user_repo.get_by_id(sub_updates["user_id"])
            if non_admin_user.role == UserRole.ADMIN:
                raise BusinessRuleError("The admin don't have subscription")

        for key, value in sub_updates.items():
            if value is not None:
                setattr(sub, key, value)

        self.db.commit()
        self.db.refresh(sub)
        return sub

    def delete(self, sub_id) -> SubscriptionOut:
        sub = self.get_by_id(sub_id)
        self.db.delete(sub)
        self.db.commit()
        return {"detail": "Subscription deleted successfully"}
