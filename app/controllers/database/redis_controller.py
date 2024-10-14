from functools import cached_property

from redis.asyncio import Redis
from loguru import logger

from app.controllers.database.base import BaseDbController


class RedisController(BaseDbController):
    def __init__(self):
        ...

    @cached_property
    def client(self):
        logger.info("Creating new Redis connection")
        return Redis(host="localhost", port=6379, decode_responses=True)
