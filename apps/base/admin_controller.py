import abc
from functools import cached_property

from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis


class BaseAppAdminController(abc.ABC):
    def __init__(self, logger):
        self.logger = logger
        ...

    @abc.abstractmethod
    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        ...

    @cached_property
    def mongo_client(self):
        self.logger.info("Creating new Mongo connection")
        return AsyncIOMotorClient(host="localhost", port=27017)

    @cached_property
    def redis_client(self):
        self.logger.info("Creating new Redis connection")
        return Redis(host="localhost", port=6379, decode_responses=True)