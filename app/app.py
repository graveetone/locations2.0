from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.constants import Action, AppCode
from app.controllers.app.base import BaseAppController
from app.controllers.app.mongo_embedded import MongoEmbeddedAppController
from app.controllers.app.mongo_normalized import MongoNormalizedAppController
from app.mongo_controller import MongoController

app = FastAPI()
mongo = MongoController("fast_locations_db", "location")
redis = None #RedisController()


APP_CONTROLLERS = {
    AppCode.MONGO_EMBEDDED: MongoEmbeddedAppController,
    AppCode.MONGO_NORMALIZED: MongoNormalizedAppController,
    AppCode.REDIS_UNKNOWN: BaseAppController,
}


@app.websocket("/ws/{app_code}")
async def ws_locations(websocket: WebSocket, app_code: AppCode):
    controller = APP_CONTROLLERS[app_code]
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            action = Action(data.pop("action"))
            response = await controller().invoke(action, **data)
            await websocket.send_json(response)

    except WebSocketDisconnect:
        print("Connection closed")
