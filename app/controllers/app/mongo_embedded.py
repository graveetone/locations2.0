from app.controllers.app.base import BaseAppController


class MongoEmbeddedAppController(BaseAppController):
    DATABASE = "embedded_app"
    COLLECTION = "resources"

    async def add_location(self, resource_id, location):
        ...

    async def get_last_location(self, resource_id):
        ...

    async def get_locations(self, resource_id):
        return {1: 2}

    async def get_resources_nearby(self, location, radius, timedelta):
        ...