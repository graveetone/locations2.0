from functools import cached_property

from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

from app.controllers.database.base import BaseDbController


class MongoController(BaseDbController):
    def __init__(self, database=None, collection=None):
        self.database = database
        self.collection = collection
        # TODO: add setters for database and collection

    async def create(self, document):
        return await self.client[self.database][self.collection].insert_one(document)

    async def find_many(self, **kwargs):
        documents = self.client[self.database][self.collection].find(kwargs, {'_id': False})
        return [document async for document in documents]

    async def find_one(self, **kwargs):
        return await self.client[self.database][self.collection].find_one(kwargs)

    @cached_property
    def client(self):
        logger.info("Creating new Mongo connection")
        return AsyncIOMotorClient(host="localhost", port=27017)
