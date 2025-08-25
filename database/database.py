from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
import logging

logger = logging.getLogger(__name__)

client = AsyncIOMotorClient(Config.mongo_uri)
db = client["url"]
collection = db["shorturl"]
