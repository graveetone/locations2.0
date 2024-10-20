import random

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppAdminController
from apps.mongo_embedded.models import Location
from constants import MONGO_EMBEDDED_APP_DATABASE
from utils.helpers import generate_random_coordinates


class MongoEmbeddedAdminController(BaseAppAdminController):
    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        resources = []

        for resource_id in range(1, number_of_resources + 1):
            locations = (
                Location(
                    point=generate_random_coordinates(),
                ) for _ in range(locations_per_resource)
            )
            locations = jsonable_encoder(parse_obj_as(list[Location], locations))

            resources.append({
                "resource_id": resource_id,
                "locations": locations
            })

        random.shuffle(resources)
        await self.mongo_client[MONGO_EMBEDDED_APP_DATABASE].resource.insert_many(resources)

        self.logger.success(f"Seeded {locations_per_resource * number_of_resources} locations")

    async def reset_database(self):
        """Drop and recreate database"""
        await self.mongo_client.drop_database(MONGO_EMBEDDED_APP_DATABASE)
        self.mongo_client[MONGO_EMBEDDED_APP_DATABASE]
