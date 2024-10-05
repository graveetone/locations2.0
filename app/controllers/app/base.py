from app.constants import Action
from app.models.point import Point


class BaseAppController:
    # rewrite to cls methods?

    # rewrite to __call__?
    async def invoke(self, action: Action, **kwargs):
        return await getattr(self, action.value)(**kwargs)

    async def get_last_location(self, resource_id: int):
        raise NotImplemented

    async def get_locations(self, resource_id: int):
        raise NotImplemented

    async def add_location(self, resource_id: int, point: Point):
        raise NotImplemented

    async def get_resources_nearby(self, point: Point, radius: float, time_threshold: float):
        raise NotImplemented
