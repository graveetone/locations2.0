import abc

import loguru
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from constants import AppCode


class BaseAppAdminController(abc.ABC):
    mongo_client: AsyncIOMotorClient
    redis_client: Redis

    def __init__(self, logger: loguru.logger, app_code: AppCode):
        self.logger = logger
        self.app_code = app_code

        self.logger = logger.bind(identifier=app_code.name)

    @abc.abstractmethod
    async def seed_database(self, number_of_resources: int, locations_per_resource: int): ...

    @abc.abstractmethod
    async def reset_database(self): ...
