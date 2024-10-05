from app.constants import AppCode
from app.controllers.app.base import BaseAppController
from app.controllers.app.mongo_embedded import MongoEmbeddedAppController
from app.controllers.app.mongo_normalized import MongoNormalizedAppController

APP_CONTROLLERS = {
    AppCode.MONGO_EMBEDDED: MongoEmbeddedAppController,
    AppCode.MONGO_NORMALIZED: MongoNormalizedAppController,
    AppCode.REDIS_UNKNOWN: BaseAppController,
}