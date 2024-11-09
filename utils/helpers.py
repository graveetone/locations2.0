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


def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='+', print_end="\r"):
    """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
            printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
        """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = BinaryColor.GREEN + fill * filled_length + BinaryColor.RED + '-' * (length - filled_length) + BinaryColor.ENDC
    print(f'\r{BinaryColor.HEADER}{prefix}{BinaryColor.ENDC} |{bar}| {percent}% {suffix}', end=print_end)

    if iteration == total:
        print()


class BinaryColor:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
