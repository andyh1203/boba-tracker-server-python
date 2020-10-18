import motor.motor_asyncio

from app.config import get_settings

settings = get_settings()

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URL)
db = client[settings.MONGO_DATABASE]
boba_collection = db["boba"]
user_collection = db["user"]
