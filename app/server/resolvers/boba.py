from typing import List
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
# from app.server.models.boba import Boba

MONGO_URL = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = client['boba-tracker-dev']

boba_collection = db['boba']

async def add_boba(data: dict) -> dict:
    await boba_collection.insert_one(data)

async def get_boba() -> List[dict]:
    return [
        boba
        async for boba in boba_collection.find()
    ]


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(add_boba({'drinkName': 'test', 'iceLevel': 'test', 'sugarLevel': 'test'}))
    print(loop.run_until_complete(get_boba()))