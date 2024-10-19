from datetime import datetime, timedelta, UTC

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppController
from apps.mongo_embedded.models import Location, Point
from constants import MONGO_EMBEDDED_APP_DATABASE
from utils.helpers import meters_to_radians


class MongoEmbeddedAppController(BaseAppController):
    async def add_location(self, resource_id: int, location: dict):
        self.logger.debug(f"Resource {resource_id} | Add location")

        location = Location(**location)
        self.resource_collection.find_one_and_update(
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

        resource = await self.resource_collection.find_one(
            {
                "resource_id": resource_id
            },
            {
                "locations": {
                    "$slice": -1
                }
            }
        )

        locations = resource.get("locations", [])
        last_location = next(iter(locations), {})
        return jsonable_encoder(Location(**last_location))

    async def get_locations(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get locations")

        resource = await self.resource_collection.find_one(
            {
                "resource_id": resource_id
            }
        )
        locations = resource.get("locations", [])
        return jsonable_encoder(parse_obj_as(list[Location], locations))

    async def get_resources_nearby(self, point: dict, radius: float, time_threshold: float):
        self.logger.debug("Get resources nearby")
        point = Point(**point)

        time_limit = datetime.now(UTC).timestamp() - time_threshold
        nearby_locations = await self.resource_collection.find(filter={
            "locations": {
                "$elemMatch": {
                    "point": {
                        "$geoWithin": {
                            "$centerSphere": [[point.longitude, point.latitude], meters_to_radians(radius=radius)]
                        }
                    },
                    "timestamp": {"$gte": time_limit}
                }
            }
        }).to_list(None)
        nearby_resources_ids = {location["resource_id"] for location in nearby_locations}

        return jsonable_encoder(nearby_resources_ids)

    @property
    def resource_collection(self):
        return self.mongo_client[MONGO_EMBEDDED_APP_DATABASE].resource
