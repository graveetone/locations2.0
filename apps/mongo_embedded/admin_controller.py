import random

from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as

from apps.base import BaseAppAdminController
from apps.mongo_embedded.models import Location
from utils.helpers import generate_random_coordinates

DATABASE = "mongo_embdedded_db"

class MongoEmbeddedAdminController(BaseAppAdminController):
    SEEDING_CHUNKS = 10000 # implement chunking logic to seed a lot of data

    async def seed_database(self, number_of_resources: int, locations_per_resource: int):
        locations = (
            Location(
                point=generate_random_coordinates(),
                resource_id=resource_id
            ) for _ in range(locations_per_resource)
            for resource_id in range(1, number_of_resources + 1)
        )
        locations = jsonable_encoder(parse_obj_as(list[Location], locations))
        random.shuffle(locations)
        await self.mongo_client[DATABASE].location.insert_many(locations)
        self.logger.success(f"Seeded {locations_per_resource * number_of_resources} locations")

