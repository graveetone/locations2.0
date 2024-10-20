import random

from constants import REDIS_LOCATIONS_PATTERN, REDIS_LAST_LOCATION_PATTERN
from apps.base import BaseAppAdminController
from utils.helpers import generate_random_coordinates
from apps.redis_list.models import Location


class RedisListAdminController(BaseAppAdminController):
    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        for resource_id in range(1, number_of_resources + 1):
            locations = [
                Location(
                    point=generate_random_coordinates(),
                    resource_id=resource_id
                ) for _ in range(locations_per_resource)
            ]
            random.shuffle(locations)
            await self.redis_client.lpush(
                REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code.value),
                *[location.json() for location in locations]
            )

            last_location_point = locations[-1].point
            await self.redis_client.geoadd(
                REDIS_LAST_LOCATION_PATTERN.format(app_code=self.app_code.value),
                (last_location_point.longitude, last_location_point.latitude, resource_id)
            )

        self.logger.success(f"Seeded {locations_per_resource * number_of_resources} locations")

    async def reset_database(self):
        keys = self.redis_client.scan_iter(f"{self.app_code.value}*")
        async for key in keys:
            await self.redis_client.delete(key)
