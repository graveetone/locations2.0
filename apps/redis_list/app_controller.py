from datetime import datetime, timedelta, UTC

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppController
from apps.redis_list.models import RedisPoint, RedisLocation
from constants import REDIS_LOCATIONS_PATTERN, REDIS_LAST_LOCATION_PATTERN


class RedisListAppController(BaseAppController):
    async def add_location(self, resource_id: int, location: dict):
        self.logger.debug(f"Resource {resource_id} | Add location")

        location = RedisLocation(**location, resource_id=resource_id)

        await self.redis_client.lpush(
            REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
            location.json()
        )

        await self.redis_client.geoadd(
            REDIS_LAST_LOCATION_PATTERN.format(app_code=self.app_code.value),
            (location.point.longitude, location.point.latitude, resource_id)
        )

        return jsonable_encoder(location)

    async def get_last_location(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get last location")

        location = await self.redis_client.lindex(
            REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
            0
        )

        return jsonable_encoder(RedisLocation.parse_raw(location))

    async def get_locations(self, resource_id: int):
        self.logger.debug(f"Resource {resource_id} | Get locations")

        locations = await self.redis_client.lrange(
            REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
            0, -1
        )
        locations = [RedisLocation.parse_raw(location) for location in locations]

        return jsonable_encoder(parse_obj_as(list[RedisLocation], locations))

    async def get_resources_nearby(self, point: dict, radius: float, time_threshold: float):
        self.logger.debug("Get resources nearby")
        point = RedisPoint(**point)

        min_timestamp = datetime.now(UTC) - timedelta(seconds=time_threshold)
        nearby_resources_ids = await self.redis_client.georadius(
            REDIS_LAST_LOCATION_PATTERN.format(app_code=self.app_code.value),
            point.longitude, point.latitude,
            radius, unit='m'
        )

        # filter by timestamp
        nearby_resources = set()
        for resource_id in nearby_resources_ids:
            last_resource_location = await self.redis_client.lindex(
                REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
                0
            )
            location_timestamp = RedisLocation.parse_raw(last_resource_location).timestamp

            if location_timestamp >= min_timestamp:
                nearby_resources.add(int(resource_id))

        return jsonable_encoder(nearby_resources)
