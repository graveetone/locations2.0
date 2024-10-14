from abc import ABC, abstractmethod

import loguru

from app.constants import Action
from app.models.mongo_normalized import Point, Resource, Location


class BaseAppController(ABC):
    def __init__(self, logger: loguru.logger):
        self.logger = logger

    async def __call__(self, action: Action, **kwargs):
        self.logger.info(f"Invocation of {self.__class__.__name__}")
        return await getattr(self, action.value)(**kwargs)


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
