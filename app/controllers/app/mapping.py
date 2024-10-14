from app.constants import AppCode
from app.controllers.app.mongo_embedded import MongoEmbeddedAppController
from app.controllers.app.mongo_normalized import MongoNormalizedAppController
from app.controllers.app.redis_list import RedisListAppController
from app.controllers.app.redis_sorted_set import RedisSortedSetAppController

APP_CONTROLLERS = {
    AppCode.MONGO_EMBEDDED: MongoEmbeddedAppController,
    AppCode.MONGO_NORMALIZED: MongoNormalizedAppController,
    AppCode.REDIS_LIST: RedisListAppController,
    AppCode.REDIS_SORTED_SET: RedisSortedSetAppController
}
