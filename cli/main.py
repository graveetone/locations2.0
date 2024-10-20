from cli.helpers import run_server, run_test_plans, parse_reports, send_metrics_to_datadog, shutdown_server, \
    get_event_loop
from utils.logger import get_logger
from constants import AppCode, Action
from mappings import ADMIN_CONTROLLERS

mongo_client = AsyncIOMotorClient(**MONGO_CONFIG)
redis_client = Redis(**REDIS_CONFIG)

async def main():
    for app_code in AppCode:
        logger.critical(app_code.name)
        admin_controller = ADMIN_CONTROLLERS[app_code](logger=logger, app_code=app_code)

        admin_controller.mongo_client = mongo_client
        admin_controller.redis_client = redis_client

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
