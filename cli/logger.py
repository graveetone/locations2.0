import sys

from loguru import logger as _logger


def get_logger(identifier):
    logger_format = (
        "<level>{level}</level>: "
        "<light-blue>{time:YYYY-MM-DD HH:mm:ss.SSS}</light-blue> <yellow>|</yellow> "
        "<cyan>{extra[identifier]}</cyan> | {message}"
    )

    _logger.remove()
    _logger.configure(extra={"identifier": ""})
    _logger.add(sys.stderr, format=logger_format)
    _logger.bind(identifier=identifier)

    return _logger
