"""
logging handling module to create custom and particular loggers.

"""

import logging
from typing import Literal

LOG_LEVEL_LITERAL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LOGGING_FORMAT: str = "{asctime} [{levelname}] - {name} : {message}"
DEFAULT_LOG_LEVEL: LOG_LEVEL_LITERAL | None = None

logging.basicConfig(format=DEFAULT_LOGGING_FORMAT, style="{")


def get_logger(
    name: str | None = None, log_level: LOG_LEVEL_LITERAL | None = DEFAULT_LOG_LEVEL
) -> logging.Logger:
    """
    get a logger object.

    Args:
        name (:obj:`str`, optional): Specify a name if you want
            to retrieve a logger which is a child of
            PostTracker logger.
        log_level (:obj:`str`, optional): Specify the log level
            for this particular logger.

    Returns:
        The PostTracker logger, or one of its children.
    """

    # create logger
    _logger_name = "PostTracker"
    if name:
        _logger_name += f".{name}"

    # create logger
    logger = logging.getLogger(name=_logger_name)
    # set log level
    if log_level is not None:
        logger.setLevel(log_level)
    logging.debug(f"logger created {logger}")

    return logger
