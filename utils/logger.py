import sys

from loguru import logger as _logger


def get_logger():
    logger_format = (
        "<level>{level}</level>: "
        "<light-blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-blue> <yellow>|</yellow> "
        "<cyan>{extra[app_code]}</cyan> | {message}"
    )

    _logger.remove()
    _logger.configure(extra={"app_code": ""})
    _logger.add(sys.stderr, format=logger_format)

    return _logger
