from abc import ABC, abstractmethod

import loguru

from app.constants import Action, AppCode
from app.models.mongo_normalized import Point, Resource, Location


class BaseAppController(ABC):
    CONTROLLER = None
    def __init__(self, logger: loguru.logger, app_code: AppCode):
        self.logger = logger
        self.app_code = app_code.value

    async def __call__(self, action: Action, **kwargs):
        self.logger.info(f"Invocation of {self.__class__.__name__}")
        return await getattr(self, action.value)(**kwargs)

    @property
    def client(self):
        return self.CONTROLLER.client

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
