import random


def meters_to_radians(radius: float):
    return radius * 1000 / 6378.1  # radius in km divided by radius of Earth


def generate_random_coordinates():
    return {
        "latitude": random.uniform(-85, 85),
        "longitude": random.uniform(-180, 180)
    }
