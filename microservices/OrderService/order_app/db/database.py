from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DATABASE_URL = "mongodb://mongodb:27017/orders"

engine = AsyncIOMotorClient(MONGO_DATABASE_URL)
database = engine.get_database()
