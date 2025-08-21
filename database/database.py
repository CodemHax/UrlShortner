from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
client = AsyncIOMotorClient(Config.mongo_uri)
db = client["url"]
collection = db["shorturl"]
