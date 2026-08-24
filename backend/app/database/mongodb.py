from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.core.config import MONGODB_URL, DATABASE_NAME


client = AsyncIOMotorClient(MONGODB_URL)

database = client[DATABASE_NAME]

# GridFS bucket for storing PDF, video and audio files
gridfs_bucket = AsyncIOMotorGridFSBucket(database)


async def connect_to_mongo():

    await client.admin.command("ping")

    print("MongoDB connected successfully")


async def close_mongo_connection():

    client.close()

    print("MongoDB connection closed")