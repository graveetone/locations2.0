import time

from automation.helpers import run_server, run_test_plans, parse_report, send_metrics_to_datadog, shutdown_server, \
    get_event_loop, rotate_reports
from config import SEED_PARAMETERS
from utils.helpers import get_mongo_client, get_redis_client
from utils.logger import get_logger
from constants import AppCode, Action
from mappings import ADMIN_CONTROLLERS


async def main():
    started_at = time.time()
    logger.info("Rotating reports")
    rotate_reports()

    logger.info("Running server")
    server_process = run_server()

    mongo_client = get_mongo_client()
    redis_client = get_redis_client()
    for seed_param in SEED_PARAMETERS:
        logger.info(f"Seeding with params: {seed_param}")
        for app_code in AppCode:
            logger.critical(app_code.name)
            admin_controller = ADMIN_CONTROLLERS[app_code](logger=logger, app_code=app_code)

            admin_controller.mongo_client = mongo_client
            admin_controller.redis_client = redis_client

            logger.info("Reset database")
            await admin_controller.reset_database()

            logger.info("Seeding db")
            await admin_controller.seed_database(
                **seed_param
            )

            for action in Action:
                logger.info(f"Running test plan for {action.name}")
                run_test_plans(app_code=app_code, action=action, seed_param=seed_param)

                logger.info("Parsing csv reports")
                report_data = parse_report(app_code=app_code, action=action, seed_param=seed_param)

                logger.info("Sending metrics to Datadog")
                send_metrics_to_datadog(report_data=report_data)

    logger.info("Shutting server down and closing db connections")
    shutdown_server(server_process=server_process)
    mongo_client.close()
    await redis_client.aclose()

    logger.success(f"Pipeline finished. Time spent: {time.time() - started_at} seconds")


if __name__ == "__main__":
    logger = get_logger(identifier="CLI")
    loop = get_event_loop()
    loop.run_until_complete(main())
