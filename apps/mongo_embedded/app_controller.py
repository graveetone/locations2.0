from datetime import datetime, timedelta, UTC

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppController
from apps.mongo_embedded.models import Location, Point
from utils.helpers import meters_to_radians

DATABASE = "mongo_embedded_db"


class MongoEmbeddedAppController(BaseAppController):
    async def add_location(self, resource_id: int, location: dict):
        self.logger.debug(f"Resource {resource_id} | Add location")

        location = Location(**location, resource_id=resource_id)
        self.resource_collection.updateOne(
            {
                "resource_id": resource_id
            },
            {
                "$push": {
                    "locations": location.model_dump()
                }
            }
        )
        return jsonable_encoder(location)

    async def get_last_location(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get last location")

        locations = await self.locations.find(
            {"resource_id": resource_id}).sort({"timestamp": -1}).limit(1).to_list(None)

        if locations:
            return jsonable_encoder(Location(**locations[0]))
        return {}

    async def get_locations(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get locations")

        locations = await self.locations.find(
            {"resource_id": resource_id}).sort({"timestamp": 1}).to_list(None)

        return jsonable_encoder(parse_obj_as(list[Location], locations))

    async def get_resources_nearby(self, point: dict, radius: float, time_threshold: float):
        self.logger.debug(f"Get resources nearby")
        point = Point(**point)

        time_limit = datetime.now(UTC) - timedelta(seconds=time_threshold)
        nearby_locations = await self.locations.find(filter={
            "point": {
                "$geoWithin": {
                    "$centerSphere": [[point.longitude, point.latitude], meters_to_radians(radius=radius)]
                }
            },
            "timestamp": {"$gte": time_limit}
        }).to_list(None)

        nearby_resources_ids = {location["resource_id"] for location in nearby_locations}

        return jsonable_encoder(nearby_resources_ids)

    @property
    def locations(self):
        return self.mongo_client[DATABASE].location

    @property
    def resource_collection(self):
        return self.mongo_client[DATABASE].resource

