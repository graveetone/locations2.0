from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from constants import Action, AppCode
from mappings import APP_CONTROLLERS
from utils.helpers import get_redis_client, get_mongo_client
from utils.logger import get_logger

app = FastAPI()


@app.websocket("/ws/{app_code}")
async def ws_locations(websocket: WebSocket, app_code: AppCode):
    app_code = AppCode(app_code)
    logger = get_logger(identifier=app_code.name)
    controller = APP_CONTROLLERS[app_code](logger=logger, app_code=app_code)
    controller.mongo_client = app.state.mongo_client
    controller.redis_client = app.state.redis_client

    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            action = Action(data.pop("action"))
            logger.info(f"Got action: {action.name}")

            response = await controller(action, **data)
            await websocket.send_json(response)

    except WebSocketDisconnect:
        logger.info("Connection closed")


@app.get("/health")
async def health_check():
    return {"status": "UP"}


@app.on_event("startup")
def create_db_connections():
    app.state.mongo_client = get_mongo_client()
    app.state.redis_client = get_redis_client()


@app.on_event("shutdown")
async def close_db_connections():
    app.state.mongo_client.close()
    await app.state.redis_client.aclose()
