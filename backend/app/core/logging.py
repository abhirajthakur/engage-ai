import logging
import sys

from app.core.config import settings


def _get_formatter() -> logging.Formatter:
    if settings.environment == "production":
        fmt = '{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}'
    else:
        fmt = "%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"
    return logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")


def get_logger(name: str) -> logging.Logger:
    """
    Usage:
        from app.core.logger import get_logger
        log = get_logger(__name__)
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(_get_formatter())
        logger.addHandler(handler)

    logger.setLevel(settings.log_level.upper())
    return logger
