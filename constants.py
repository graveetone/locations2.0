from enum import Enum


class Action(Enum):
    ADD_LOCATION: str = "add_location"
    GET_LAST_LOCATION: str = "get_last_location"
    GET_LOCATIONS: str = "get_locations"
    GET_RESOURCES_NEARBY: str = "get_resources_nearby"


class AppCode(Enum):
    MONGO_EMBEDDED: str = "mongo_embedded"
    MONGO_NORMALIZED: str = "mongo_normalized"
    REDIS_LIST: str = "redis_list"
    REDIS_SORTED_SET: str = "redis_sorted_set"


MONGO_EMBEDDED_APP_DATABASE = "mongo_embedded_db"
MONGO_NORMALIZED_APP_DATABASE = "mongo_normalized_db"

REDIS_LOCATIONS_PATTERN = "{app_code}::resource::{resource_id}::locations"
REDIS_LAST_LOCATION_PATTERN = "{app_code}::last_locations"
