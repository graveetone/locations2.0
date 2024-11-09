import random

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppAdminController
from constants import MONGO_NORMALIZED_APP_DATABASE
from utils.helpers import generate_random_coordinates, print_progress_bar
from apps.mongo_normalized.models import Location


class MongoNormalizedAdminController(BaseAppAdminController):

    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        all_locations = []
        for resource_id in range(1, number_of_resources + 1):
            locations = (
                Location(
                    point=generate_random_coordinates(),
                    resource_id=resource_id
                ) for _ in range(locations_per_resource)
            )

            all_locations.extend(jsonable_encoder(parse_obj_as(list[Location], locations)))
            print_progress_bar(iteration=resource_id, total=number_of_resources)

        random.shuffle(all_locations)
        await self.mongo_client[MONGO_NORMALIZED_APP_DATABASE].location.insert_many(all_locations)

        self.logger.success(f"Seeded {len(all_locations)} locations")

    async def reset_database(self):
        """Drop and recreate database"""
        await self.mongo_client.drop_database(MONGO_NORMALIZED_APP_DATABASE)
        self.mongo_client[MONGO_NORMALIZED_APP_DATABASE]
