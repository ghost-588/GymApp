from datetime import datetime
from typing import Annotated
from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import timedelta, timezone
from dotenv import load_dotenv
from passlib.context import CryptContext
import re

from sqlalchemy.orm import Session
from app.database import get_db
from app.exceptions.exceptions import InvalidCredentials, InvalidToken
from app.repositories.users_repositories import UserRepository
import os


router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

load_dotenv()

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")

login_form_data = Annotated[OAuth2PasswordRequestForm, Depends()]
db_depends = Annotated[Session, Depends(get_db)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS"))
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM")
    )
    return encoded_jwt


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        return payload
    except JWTError:
        raise InvalidToken("Invalid or expired token")


@router.post("/login")
async def login(form_data: login_form_data, db: db_depends):
    email = form_data.username
    password = form_data.password

    if not email_pattern.match(email):
        raise InvalidCredentials("Incorrect username or password")

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)

    if not pwd_context.verify(password, user.hashed_password):
        raise InvalidCredentials("Incorrect username or password")

    data = {
        "sub": str(user.id),
        "role": user.role.value,
    }

    access_token = create_access_token(data)
    refresh_token = create_refresh_token(data)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


async def get_current_user(
    token: Annotated[str, Depends(oauth2_bearer)], db: db_depends
):
    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise InvalidToken("Invalid token")

        user_repo = UserRepository(db)
        user = user_repo.get_by_id(int(user_id))
        return user

    except JWTError:
        raise InvalidToken("Invalid or expired token")


@router.post("/refresh")
async def refresh(refresh_token: str):
    payload = verify_token(refresh_token)
    user_id = payload.get("sub")
    if not user_id:
        raise InvalidToken("Invalid refresh token")

    new_access_token = create_access_token(payload)
    return {"access_token": new_access_token, "token_type": "bearer"}
