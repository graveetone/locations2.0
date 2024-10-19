from apps.mongo_embedded import MongoEmbeddedAppController, MongoEmbeddedAdminController
from apps.mongo_normalized import MongoNormalizedAppController, MongoNormalizedAdminController
from apps.redis_list import RedisListAppController, RedisListAdminController
from apps.redis_sorted_set import RedisSortedSetAppController, RedisSortedSetAdminController
from constants import AppCode

APP_CONTROLLERS = {
    AppCode.MONGO_EMBEDDED: MongoEmbeddedAppController,
    AppCode.MONGO_NORMALIZED: MongoNormalizedAppController,
    AppCode.REDIS_LIST: RedisListAppController,
    AppCode.REDIS_SORTED_SET: RedisSortedSetAppController
}

ADMIN_CONTROLLERS = {
    AppCode.MONGO_EMBEDDED: MongoEmbeddedAdminController,
    AppCode.MONGO_NORMALIZED: MongoNormalizedAdminController,
    AppCode.REDIS_LIST: RedisListAdminController,
    AppCode.REDIS_SORTED_SET: RedisSortedSetAdminController
}
