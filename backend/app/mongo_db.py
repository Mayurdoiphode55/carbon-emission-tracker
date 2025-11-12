from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB", "carbon_tracker")

client = AsyncIOMotorClient(MONGO_URI)
mongo_db = client[DB_NAME]
