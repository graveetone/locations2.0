from datetime import datetime, timedelta, UTC

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from app.controllers.app.base import BaseAppController
from app.controllers.database.mongo_controller import MongoController
from app.models.mongo_normalized import Location, Resource, Point


def meters_to_radians(radius: float):
    return radius * 1000 / 6378.1  # radius in km divided by radius of Earth


class MongoNormalizedAppController(BaseAppController):
    DB = "mongo_normalized_db"
    CONTROLLER = MongoController(database=DB)

    @property
    def database(self):
        return self.CONTROLLER.client[self.DB]

    async def add_location(self, resource_id: int, location: dict):
        self.logger.debug(f"Resource {resource_id} | Add location")

        location = Location(**location)
        resource = await self.find_resource(identifier=resource_id)

        location.resource_id = resource.mongo_id

        result = await self.database.location.insert_one(location.model_dump())
        created_location = await self.database.location.find_one({"_id": result.inserted_id})

        return jsonable_encoder(Location(**created_location))

    async def get_last_location(self, resource_id):
        self.logger.debug(f"Resource {resource_id} | Get last location")

        resource = await self.find_resource(identifier=resource_id)

        locations = await self.database.location.find(
            {"resource_id": resource.mongo_id}).sort({"timestamp": -1}).limit(1).to_list(None)
        if locations:
            return jsonable_encoder(Location(**locations[0]))
        return {}

    async def get_locations(self, resource_id):
        self.logger.debug(f"Resource {resource_id} | Get locations")

        resource = await self.find_resource(identifier=resource_id)

        locations = await self.database.location.find(
            {"resource_id": resource.mongo_id}).sort({"timestamp": 1}).to_list(None)

        return jsonable_encoder(parse_obj_as(list[Location], locations))

    async def get_resources_nearby(self, point, radius, time_threshold):
        self.logger.debug(f"Get resources nearby")
        point = Point(**point)

        time_limit = datetime.now(UTC) - timedelta(seconds=time_threshold)
        nearby_locations = await self.database.location.find(filter={
            "point": {
                "$geoWithin": {
                    "$centerSphere": [[point.longitude, point.latitude], meters_to_radians(radius=radius)]
                }
            },
            "timestamp": {"$gte": time_limit}
        }).to_list(None)

        nearby_resources_ids = [location["resource_id"] for location in nearby_locations]
        resources_nearby = await self.database.resource.find({"_id": {"$in": nearby_resources_ids}}).to_list(None)

        return jsonable_encoder(parse_obj_as(list[Resource], resources_nearby))

    async def find_resource(self, identifier: int):
        resource = await self.database.resource.find_one({"identifier": identifier})
        return Resource(**resource)
