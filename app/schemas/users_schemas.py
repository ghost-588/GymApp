import re
from pydantic import BaseModel, EmailStr, Field, StringConstraints, field_validator
from typing import Annotated, Optional

from app.models.users_model import UserRole

name_pattern = re.compile(r"^[A-Za-z\u0600-\u06FF\s]+$")
phone_number_pattern = re.compile(r"^\d{7,15}$")


class UserCreate(BaseModel):
    first_name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=2, max_length=50),
        Field(description="First name in Arabic or English, 2-50 chars"),
    ]

    last_name: Annotated[
        str,
        StringConstraints(strip_whitespace=True, min_length=2, max_length=50),
        Field(description="Last name in Arabic or English, 2-50 chars"),
    ]

    email: Annotated[EmailStr, Field(description="Valid email address")]

    password: Annotated[
        str,
        StringConstraints(min_length=8),
        Field(
            description="At least 8 chars, must include an uppercase letter and a digit"
        ),
    ]

    role: UserRole

    phone_number: Annotated[
        str,
        StringConstraints(strip_whitespace=True),
        Field(description="Must be a valid phone number"),
    ]

    model_config = {"from_attributes": True}

    @field_validator("first_name")
    def validate_first_name(cls, value: str) -> str:
        if not name_pattern.match(value):
            raise ValueError("First name must contain only Arabic and English letters")
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value: str) -> str:
        if not name_pattern.match(value):
            raise ValueError("Last name must contain only Arabic and English letters")
        return value

    @field_validator("password")
    def validate_password_strength(cls, value: str):
        if (not re.search(r"\d", value)) or (not re.search(r"[A-Z]", value)):
            raise ValueError(
                "The password must contain at least on uppercase letter and one digit"
            )
        return value

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str):
        value = value.strip()
        if value.startswith("+"):
            value = value[1:]

        if not phone_number_pattern.match(value):
            raise ValueError("Phone number must be a valid phone number")
        return value


class UserUpdate(BaseModel):
    first_name: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True, min_length=2, max_length=50),
        Field(None, description="First name in Arabic or English, 2-50 chars"),
    ]

    last_name: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True, min_length=2, max_length=50),
        Field(None, description="Last name in Arabic or English, 2-50 chars"),
    ]

    email: Annotated[Optional[EmailStr], Field(None, description="Valid email address")]

    password: Annotated[
        Optional[str],
        StringConstraints(min_length=8),
        Field(
            None,
            description="At least 8 chars, must include an uppercase letter and a digit",
        ),
    ]

    role: Annotated[Optional[UserRole], Field(None)]

    phone_number: Annotated[
        Optional[str],
        StringConstraints(strip_whitespace=True),
        Field(None, description="Must be a valid phone number"),
    ]

    model_config = {"from_attributes": True}

    @field_validator("first_name")
    def validate_first_name(cls, value: str) -> str:
        if value and not name_pattern.match(value):
            raise ValueError("First name must contain only Arabic and English letters")
        return value

    @field_validator("last_name")
    def validate_last_name(cls, value: str) -> str:
        if value and not name_pattern.match(value):
            raise ValueError("Last name must contain only Arabic and English letters")
        return value

    @field_validator("password")
    def validate_password_strength(cls, value: str):
        if value and (not re.search(r"\d", value)) or (not re.search(r"[A-Z]", value)):
            raise ValueError(
                "The password must contain at least on uppercase letter and one digit"
            )
        return value

    @field_validator("phone_number")
    def validate_phone_number(cls, value: str):
        value = value.strip()
        if value and value.startswith("+"):
            value = value[1:]

        if value and not phone_number_pattern.match(value):
            raise ValueError("Phone number must be a valid phone number")
        return value


class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone_number: str
    role: UserRole
    hashed_password: str

    model_config = {"from_attributes": True}
