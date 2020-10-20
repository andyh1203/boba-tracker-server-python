from pydantic import BaseModel, ValidationError, validator
from app.server.database import user_collection
from typing import List


class RegisterInput(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @validator("first_name", "last_name")
    def name_length(cls, v):
        if len(v) < 1:
            raise ValueError("Length must be greater than 1")
        return v

    # Can't run async validators?
    # @validator("email")
    # async def unique_email(cls, v):
    #     user = await user_collection.find_one({"email": v})
    #     print(user)
    #     if not user:
    #         raise ValueError("The email must be unique")
    #     return v

    @validator("email")
    def is_email(cls, v):
        if "@" not in v:
            raise ValueError("Not an email")
        return v

    @validator("password")
    def password_length(cls, v):
        if len(v) < 8:
            print("in here")
            raise ValueError("Lenght must be greater than 8")
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
