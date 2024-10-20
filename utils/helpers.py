import random

from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from config import REDIS_CONFIG, MONGO_CONFIG


def meters_to_radians(radius: float):
    return radius * 1000 / 6378.1  # radius in km divided by radius of Earth


def generate_random_coordinates():
    return {
        "latitude": random.uniform(-85, 85),
        "longitude": random.uniform(-180, 180)
    }


def get_mongo_client():
    return AsyncIOMotorClient(**MONGO_CONFIG)


def get_redis_client():
    return Redis(**REDIS_CONFIG)
