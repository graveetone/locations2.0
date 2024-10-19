import asyncio
import subprocess
import time

import requests

from cli.admin import clear_mongo, clear_redis
from cli.logger import get_logger
from constants import AppCode
from mappings import ADMIN_CONTROLLERS

path_to_app = "main.py"
RUN_SERVER_COMMAND = ["fastapi", "run", path_to_app]
SERVER_START_STOP_TIMEOUT = 2


def run_server():
    logger.info("Running server")

    server_process = subprocess.Popen(RUN_SERVER_COMMAND)
    time.sleep(SERVER_START_STOP_TIMEOUT)
    return server_process


def run_test_plans():
    logger.info("Running test plans")
    logger.success(requests.get("http://0.0.0.0:8000/health").json())


def parse_reports():
    logger.info("Parsing csv reports")


def send_metrics_to_datadog():
    logger.info("Sending metrics to Datadog")


def shutdown_server(server_process: subprocess.Popen):
    logger.info("Shutting server down")
    server_process.terminate()
    time.sleep(SERVER_START_STOP_TIMEOUT)  # wait for server to shut down


def get_event_loop():
    try:
        _loop = asyncio.get_running_loop()
    except RuntimeError:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)

    return _loop


async def main():
    for app_code in AppCode:
        logger.critical(app_code.name)
        admin_controller = ADMIN_CONTROLLERS[app_code](logger=logger, app_code=app_code)

        logger.info("Reset database")
        await admin_controller.reset_database()

        logger.info("Seeding db")
        await admin_controller.seed_database(
            number_of_resources=1000,
            locations_per_resource=10
        )
        # return
        continue
        server_process = run_server()
        time.sleep(SERVER_START_STOP_TIMEOUT)  # wait for server to start

        run_test_plans()

        parse_reports()

        send_metrics_to_datadog()

        shutdown_server(server_process=server_process)


if __name__ == "__main__":
    logger = get_logger(identifier="CLI")
    logger.info("Running pipeline with parameters: {parameters}")

    loop = get_event_loop()

    loop.run_until_complete(main())
