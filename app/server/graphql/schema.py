from app.server.utils import add_created_at_updated_at
from ariadne import (
    gql,
    QueryType,
    make_executable_schema,
    convert_kwargs_to_snake_case,
)
from ariadne import MutationType
from ariadne.scalars import ScalarType

from fastapi.responses import ORJSONResponse
from typing import List

from pydantic.error_wrappers import ValidationError
from app.server.database import boba_collection, user_collection
from app.utils.log import get_logger
from datetime import datetime
from bson.objectid import ObjectId
from app.server.schemas.user import RegisterInput
from app.server.utils.validate import validate_register
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from humps import camelize

log = get_logger()

type_defs = gql(
    """
    type Boba {
        _id: String!
        drinkName: String!
        iceLevel: String!
        sugarLevel: String!
        createdAt: DateTime!
        updatedAt: DateTime!
    }

    type User {
        _id: String!
        firstName: String!
        lastName: String!
        email: String!
        bobas: [Boba!]!
        likes: [String!]!
        createdAt: DateTime!
        updatedAt: DateTime!
    }

    scalar DateTime

    type Query {
        hello: String!
        bobas: [Boba!]
        boba(bobaId: String!): Boba
        me: User
    }

    type Mutation {
        addBoba(data: BobaInput!): Boba!
        login(email: String!, password: String!): UserResponse!
        changePassword(token: String!, password: String!): UserResponse!
        forgotPassword(email: String!): Boolean!
        logout: Boolean!
        register(data: RegisterUserInput!): UserResponse!
    }

    input RegisterUserInput {
        firstName: String!
        lastName: String!
        email: String!
        password: String!
    }

    type UserResponse {
        errors: [FieldError!]
        user: User
    }

    type BobaResponse {
        errors: [FieldError]
        boba: Boba
    }

    type FieldError {
        type: String!
        field: String!
        message: String!
    }

    input BobaInput {
        drinkName: String!
        iceLevel: String!
        sugarLevel: String!
    }
"""
)

query = QueryType()
mutation = MutationType()
datetime_scaler = ScalarType("DateTime")


@datetime_scaler.serializer
def serialize_datetime(value):
    return value.isoformat()


@query.field("bobas")
async def resolve_bobas(_, info):
    return [boba async for boba in boba_collection.find()]


@query.field("boba")
@convert_kwargs_to_snake_case
async def resolve_boba(_, info, boba_id):
    print(boba_id)
    boba = await boba_collection.find_one({"_id": ObjectId(boba_id)})
    print(boba)
    return boba


@mutation.field("addBoba")
async def resolve_add_boba(_, info, data):
    data = add_created_at_updated_at(data)
    boba = await boba_collection.insert_one(camelize(data))
    return await boba_collection.find_one({"_id": boba.inserted_id})


@mutation.field("register")
@convert_kwargs_to_snake_case
async def resolve_register(_, info, data: RegisterInput):
    user = await user_collection.find_one({"email": data["email"]})
    if user:
        return {
            "errors": [
                {
                    "type": "email_exists",
                    "field": "email",
                    "message": "That email already exists",
                }
            ]
        }
    try:
        RegisterInput(**data)
    except ValidationError as e:
        return {
            "errors": [
                {
                    "type": error["type"],
                    "field": error["loc"][0],
                    "message": error["msg"],
                }
                for error in e.errors()
            ]
        }
    else:
        hashed_password = PasswordHasher().hash(data["password"])
        data["password"] = hashed_password
        data = add_created_at_updated_at(data)
        user = await user_collection.insert_one(camelize(data))
        added_user = await user_collection.find_one({"_id": user.inserted_id})
        print(added_user)
        return {"user": added_user}


@mutation.field("login")
async def login(_, info, email: str, password: str):
    print(info.context["request"])
    print(dir(info.context["request"]))
    user = await user_collection.find_one({"email": email})
    if not user:
        return {
            "errors": [
                {
                    "type": "user_not_found",
                    "field": "email",
                    "message": "User not found",
                }
            ]
        }
    try:
        PasswordHasher().verify(user["password"], password)
    except VerifyMismatchError:
        return {
            "errors": [
                {
                    "type": "incorrect_password",
                    "field": "password",
                    "message": "Incorrect password",
                }
            ]
        }
    return {"user": user}


schema = make_executable_schema(type_defs, [query, mutation])
