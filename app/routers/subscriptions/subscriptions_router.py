from typing import List
from fastapi import APIRouter, Depends

from app.repositories.subscriptions_repositories import SubscriptionRepository
from app.schemas.subscription_schemas import (
    SubscriptionCreate,
    SubscriptionOut,
    SubscriptionUpdate,
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])


@router.get("", response_model=List[SubscriptionOut])
def get_all_subscriptions(repo: SubscriptionRepository = Depends()):
    return repo.get_all()


@router.get("/{sub_id}", response_model=SubscriptionOut)
def get_subscription_by_id(sub_id: int, repo: SubscriptionRepository = Depends()):
    return repo.get_by_id(sub_id)


@router.post("/", response_model=SubscriptionOut)
def create_subscription(
    sub_data: SubscriptionCreate, repo: SubscriptionRepository = Depends()
):
    return repo.create(sub_data.model_dump())


@router.put("/{sub_id}", response_model=SubscriptionOut)
def update_suscription(
    sub_id: int,
    sub_updates: SubscriptionUpdate,
    repo: SubscriptionRepository = Depends(),
):
    return repo.update(sub_id, sub_updates.model_dump())


@router.delete("/{sub_id}")
def delete_subscription(sub_id, repo: SubscriptionRepository = Depends()):
    return repo.delete(sub_id)
