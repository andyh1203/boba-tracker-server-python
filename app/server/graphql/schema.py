from ariadne import gql, QueryType, make_executable_schema, convert_kwargs_to_snake_case
from ariadne import MutationType
from ariadne.scalars import ScalarType

from typing import List
from app.server.models.boba import Boba
from app.server.database import boba_collection, user_collection
from app.utils.log import get_logger
from datetime import datetime
from bson.objectid import ObjectId

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

    scalar DateTime

    type Query {
        hello: String!
        bobas: [Boba!]
        boba(bobaId: String!): Boba
    }

    type Mutation {
        addBoba(data: BobaInput!): Boba!
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
async def resolve_bobas(_, info) -> List[Boba]:
    return [boba async for boba in boba_collection.find()]


@query.field("boba")
@convert_kwargs_to_snake_case
async def resolve_boba(_, info, boba_id) -> Boba:
    print(boba_id)
    boba = await boba_collection.find_one({"_id": ObjectId(boba_id)})
    print(boba)
    return boba


@mutation.field("addBoba")
async def resolve_add_boba(_, info, data: Boba):
    timestamp = datetime.now().isoformat()
    for timestamp_col in ("createdAt", "updatedAt"):
        data[timestamp_col] = timestamp
    boba = await boba_collection.insert_one(data)
    return await boba_collection.find_one({"_id": boba.inserted_id})


schema = make_executable_schema(type_defs, [query, mutation])
