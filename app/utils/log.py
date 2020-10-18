import logging
from logging import Logger

def get_logger() -> Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger
