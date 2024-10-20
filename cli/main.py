from cli.helpers import run_server, run_test_plans, parse_reports, send_metrics_to_datadog, shutdown_server, \
    get_event_loop
from utils.helpers import get_mongo_client, get_redis_client
from utils.logger import get_logger
from constants import AppCode, Action
from mappings import ADMIN_CONTROLLERS


async def main():
    logger.info("Running server")
    server_process = run_server()

    mongo_client = get_mongo_client()
    redis_client = get_redis_client()

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

        for action in Action:
            logger.info(f"Running test plan for {action.name}")
            run_test_plans(app_code=app_code, action=action)

            logger.info("Parsing csv reports")
            parse_reports()

            logger.info("Sending metrics to Datadog")
            send_metrics_to_datadog()

    logger.info("Shutting server down and closing db connections")
    shutdown_server(server_process=server_process)
    mongo_client.close()
    await redis_client.aclose()


if __name__ == "__main__":
    logger = get_logger(identifier="CLI")
    logger.info("Running pipeline with parameters: {parameters}")

    loop = get_event_loop()

    loop.run_until_complete(main())
