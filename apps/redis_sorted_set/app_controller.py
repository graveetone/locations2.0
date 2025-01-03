from datetime import datetime, UTC

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppController
from apps.redis_sorted_set.models import Location, Point
from constants import REDIS_LAST_LOCATION_PATTERN, REDIS_LOCATIONS_PATTERN


class RedisSortedSetAppController(BaseAppController):
    async def add_location(self, resource_id: int, location: dict):
        self.logger.debug(f"Resource {resource_id} | Add location")
        location = Location(**location, resource_id=resource_id)

        await self.redis_client.zadd(
            REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
            {location.json(): location.timestamp}
        )

        await self.redis_client.geoadd(
            REDIS_LAST_LOCATION_PATTERN.format(app_code=self.app_code.value),
            (location.point.longitude, location.point.latitude, resource_id)
        )

        return jsonable_encoder(location)

    async def get_last_location(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get last location")
        locations = await self.redis_client.zrevrange(
            REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
            0, 0
        )

        if not locations:
            return []

        return jsonable_encoder(Location.parse_raw(locations[0]))

    async def get_locations(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get locations")

        locations = await self.redis_client.zrevrange(
            REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
            0, -1
        )

        locations = [Location.parse_raw(location) for location in locations]

        return jsonable_encoder(parse_obj_as(list[Location], locations))

    async def get_resources_nearby(self, point: dict, radius: float, time_threshold: float):
        self.logger.debug("Get resources nearby")
        point = Point(**point)

        time_limit = datetime.now(UTC).timestamp() - time_threshold
        nearby_resources_ids = await self.redis_client.georadius(
            REDIS_LAST_LOCATION_PATTERN.format(app_code=self.app_code.value),
            point.longitude, point.latitude,
            radius, unit='m'
        )

        # filter by timestamp
        nearby_resources = set()
        for resource_id in nearby_resources_ids:
            last_resource_location = await self.redis_client.zrevrange(
                REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
                0, 0
            )
            location_timestamp = Location.parse_raw(last_resource_location[0]).timestamp

            if location_timestamp >= time_limit:
                nearby_resources.add(int(resource_id))

        return jsonable_encoder(nearby_resources)
