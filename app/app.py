from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.constants import Action, AppCode
from app.controllers.app.mapping import APP_CONTROLLERS
from app.utils.logger import get_logger

app = FastAPI()
logger = get_logger()


@app.websocket("/ws/{app_code}")
async def ws_locations(websocket: WebSocket, app_code: AppCode):
    controller = APP_CONTROLLERS[app_code]
    log = logger.bind(app_code=AppCode(app_code).name)
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            action = Action(data.pop("action"))
            log.info(action.name)

            response = await controller(logger=log).invoke(action, **data)
            await websocket.send_json(response)

    except WebSocketDisconnect:
        log.info("Connection closed")
