from app.controllers.app.base import BaseAppController


class MongoNormalizedAppController(BaseAppController):
    async def add_location(self, resource_id, location):
        ...

    async def get_last_location(self, resource_id):
        ...

    async def get_locations(self, resource_id):
        ...

    async def get_resources_nearby(self, location, radius, timedelta):
        ...