from pydantic import BaseModel, ValidationError, validator
from app.server.database import user_collection
from typing import List


def check_name_length(name: str) -> str:
    if len(name) < 1:
        raise ValidationError("Length must be greater than 1")
    return name


class RegisterInput(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    _check_first_name = validator("first_name", allow_reuse=True)(check_name_length)
    _check_last_name = validator("last_name", allow_reuse=True)(check_name_length)

    # @validator("email")
    # async def unique_email(cls, v):
    #     user = await user_collection.find({"email": v})
    #     if not user:
    #         raise ValidationError("The email must be unique")
    #     return v

    @validator("email")
    def is_email(cls, v):
        if "@" not in v:
            raise ValidationError("Not an email")
        return v

    @validator("password")
    def password_length(cls, v):
        if len(v) < 8:
            raise ValidationError("Lenght must be greater than 8")
        return v


# class User(BaseModel):
#     _id:
#     first_name: str
#     last_name: str
#     email: str
#     password: str


# class UserResponse(BaseModel):
#     errors: List[FieldError] = None
#     user:
