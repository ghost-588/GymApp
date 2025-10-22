from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.users_schemas import UserOut


class SubscriptionCreate(BaseModel):
    start: datetime
    end: datetime
    price: int
    is_active: bool
    user_id: int

    model_config = {"from_attributes": True}


class SubscriptionUpdate(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None
    price: Optional[int] = None
    is_active: Optional[bool] = None
    user_id: Optional[int] = None

    model_config = {"from_attributes": True}


class SubscriptionOut(BaseModel):
    id: int
    start: datetime
    end: datetime
    price: int
    is_active: bool
    user: UserOut
