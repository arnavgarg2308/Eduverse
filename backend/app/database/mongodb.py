from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from app.core.config import MONGODB_URL, DATABASE_NAME


client = AsyncIOMotorClient(MONGODB_URL)

database = client[DATABASE_NAME]


class GridFSBucketProxy:
    def __getattr__(self, name):
        bucket = AsyncIOMotorGridFSBucket(database)
        return getattr(bucket, name)


gridfs_bucket = GridFSBucketProxy()


async def connect_to_mongo():
    await client.admin.command("ping")

    print("MongoDB connected successfully")


async def close_mongo_connection():
    client.close()

    print("MongoDB connection closed")