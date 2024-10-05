import sys

from loguru import logger


def get_logger():
    logger_format = (
        "<level>{level}</level>: "
        "<light-blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-blue> | "
        "<cyan>{extra[app_code]}</cyan> | {message}"
    )

    logger.remove()
    logger.configure(extra={"app_code": ""})
    logger.add(sys.stderr, format=logger_format)

    return logger
