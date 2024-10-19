from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from cli.logger import get_logger


async def clear_mongo():
    logger = get_logger(identifier="CLEAR_MONGO")

    client = AsyncIOMotorClient(host="localhost", port=27017)
    databases = await client.list_database_names()

    logger.info(f"Dropping mongo databases: {databases}")
    for db_name in databases:
        if db_name in ["admin", "local", "config"]:
            continue

        await client.drop_database(db_name)


async def clear_redis():
    logger = get_logger(identifier="CLEAR_REDIS")
    client = Redis(host="localhost", port=6379, decode_responses=True)
    logger.info("Deleting all Redis keys")

    await client.flushall()
