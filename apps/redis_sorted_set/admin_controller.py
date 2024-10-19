import random
from datetime import datetime

from constants import AppCode, REDIS_LAST_LOCATION_PATTERN, REDIS_LOCATIONS_PATTERN
from apps.base import BaseAppAdminController
from utils.helpers import generate_random_coordinates
from apps.redis_sorted_set.models import RedisLocation


class RedisSortedSetAdminController(BaseAppAdminController):
    app_code = AppCode.REDIS_SORTED_SET.value

    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        for resource_id in range(1, number_of_resources + 1):
            locations = [
                RedisLocation(
                    point=generate_random_coordinates(),
                    resource_id=resource_id
                ) for _ in range(locations_per_resource)
            ]
            random.shuffle(locations)
            await self.redis_client.zadd(
                REDIS_LOCATIONS_PATTERN.format(resource_id=resource_id, app_code=self.app_code),
                mapping={location.json(): datetime.timestamp(location.timestamp) for location in locations}
            )

            last_location_point = locations[-1].point
            await self.redis_client.geoadd(
                REDIS_LAST_LOCATION_PATTERN.format(app_code=self.app_code),
                (last_location_point.longitude, last_location_point.latitude, resource_id)
            )

        self.logger.success(f"Seeded {locations_per_resource * number_of_resources} locations")
