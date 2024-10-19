import random

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppAdminController
from utils.helpers import generate_random_coordinates
from apps.mongo_normalized.models import Location, Resource


class MongoNormalizedAdminController(BaseAppAdminController):
    DB = "mongo_normalized_db"
    SEEDING_CHUNKS = 10000  # implement chunking logic to seed a lot of data

    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        resources = (Resource(identifier=identifier) for identifier in range(1, number_of_resources + 1))
        resources = jsonable_encoder(parse_obj_as(list[Resource], resources))
        for resource in resources:
            resource.pop("_id")
        random.shuffle(resources)
        resources = await self.mongo_client[self.DB].resource.insert_many(resources)

        for resource_id in resources.inserted_ids:
            locations = (
                Location(
                    point=generate_random_coordinates(),
                    resource_id=resource_id
                ) for _ in range(locations_per_resource)
            )

            locations = jsonable_encoder(parse_obj_as(list[Location], locations))
            random.shuffle(locations)
            await self.mongo_client[self.DB].location.insert_many(locations)

        self.logger.success(f"Seeded {locations_per_resource * number_of_resources} locations")