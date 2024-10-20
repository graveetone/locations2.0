from abc import ABC, abstractmethod

import loguru
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from constants import Action, AppCode


class BaseAppController(ABC):
    mongo_client: AsyncIOMotorClient
    redis_client: Redis

    def __init__(self, logger: loguru.logger, app_code: AppCode):
        self.logger = logger
        self.app_code = app_code

    async def __call__(self, action: Action, **kwargs):
        self.logger.info(f"Invocation of {self.__class__.__name__}")
        return await getattr(self, action.value)(**kwargs)

    @abstractmethod
    async def get_last_location(self, resource_id: int): ...

    @abstractmethod
    async def get_locations(self, resource_id: int): ...

    @abstractmethod
    async def add_location(self, resource_id: int, location: dict): ...

    @abstractmethod
    async def get_resources_nearby(self, point: dict, radius: float, time_threshold: float): ...
