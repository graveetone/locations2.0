from datetime import datetime, timedelta

from app.controllers.app.base import BaseAppController
from app.controllers.database.mongo_controller import MongoController


class MongoNormalizedAppController(BaseAppController):
    DB = "mongo_normalized_db"
    CONTROLLER = MongoController(database=DB)

    @property
    def database(self):
        return self.CONTROLLER.client[self.DB]

    async def add_location(self, resource_id, location):
        self.logger.debug(f"Resource {resource_id} | Add location")

        location.update({
            "timestamp": datetime.utcnow(),
            "resource_id": resource_id
        })

        created_location = await self.database.location.insert_one(location)

        # return location instead of id
        return str(created_location.inserted_id)

    async def get_last_location(self, resource_id):
        self.logger.debug(f"Resource {resource_id} | Get last location")

        locations = await self.database.location.find(
            {"resource_id": resource_id}).sort({"timestamp": -1}).limit(1).to_list(None)

        if locations:
            # return location instead of id
            return str(locations[0]["_id"])
        return {}

    async def get_locations(self, resource_id):
        self.logger.debug(f"Resource {resource_id} | Get locations")

        locations = await self.database.location.find(
            {"resource_id": resource_id}).sort({"timestamp": 1}).to_list(None)

        # return list of locations instead of ids
        return [str(location["_id"]) for location in locations]

    async def get_resources_nearby(self, location, radius, time_threshold):
        self.logger.debug(f"Get resources nearby")

        time_limit = datetime.utcnow() - timedelta(seconds=time_threshold)
        nearby_locations = await self.database.location.find({
            "point": {
                "$geoWithin": {
                    "$centerSphere": [[location['point']['longitude'], location['point']['latitude']], radius / 6378.1]  # radius in radians
                }
            },
            "timestamp": {"$gte": time_limit}
        }).to_list(None)

        # return list of resources instead of ids
        return list(set((location["resource_id"] for location in nearby_locations)))
