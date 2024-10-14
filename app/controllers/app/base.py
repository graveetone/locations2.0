from abc import ABC, abstractmethod
from functools import cached_property

import loguru
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis


from app.constants import Action, AppCode
from app.models.mongo_normalized import Point, Resource, Location


class BaseAppController(ABC):
    def __init__(self, logger: loguru.logger, app_code: AppCode):
        self.logger = logger
        self.app_code = app_code.value

    async def __call__(self, action: Action, **kwargs):
        self.logger.info(f"Invocation of {self.__class__.__name__}")
        return await getattr(self, action.value)(**kwargs)

    @cached_property
    def mongo_client(self):
        self.logger.info("Creating new Mongo connection")
        return AsyncIOMotorClient(host="localhost", port=27017)

    @cached_property
    def redis_client(self):
        self.logger.info("Creating new Redis connection")
        return Redis(host="localhost", port=6379, decode_responses=True)

    @abstractmethod
    async def get_last_location(self, resource_id: int):
        ...

    @abstractmethod
    async def get_locations(self, resource_id: int):
        ...

    @abstractmethod
    async def add_location(self, resource_id: int, location: dict):
        ...

    @abstractmethod
    async def get_resources_nearby(self, point: dict, radius: float, time_threshold: float):
        ...
