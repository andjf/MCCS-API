import logging


def create_logger(name: str, level: int = logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger
