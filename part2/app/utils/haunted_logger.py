# app/utils/haunted_logger.py
"""Spooky spells module for our haunted logging system! 👻"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    """Initialize our haunted logging system! 🎭"""
    # Max size 1MB, keep 3 backup files
    MAX_BYTES = 1_048_576  # 1MB in bytes
    BACKUP_COUNT = 3

    # Create log directories if they don't exist
    for log_type in ["api", "models", "validation"]:
        for level in ["debug", "info", "error"]:
            log_path = Path(f"logs/{log_type}/{level}.log")
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.touch()

    # Setup loggers for each component
    setup_component_logger("models")
    setup_component_logger("api")
    setup_component_logger("validation")


def setup_component_logger(component: str):
    """Setup logger for a specific component! 🎭"""
    logger_name = f"hbnb_{component}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # Create formatters
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Setup handlers with level filtering
    handlers = {
        "debug": (logging.DEBUG, lambda r: r.levelno == logging.DEBUG),
        "info": (logging.INFO, lambda r: r.levelno == logging.INFO),
        "error": (logging.ERROR, lambda r: r.levelno >= logging.ERROR),
    }

    for level, (log_level, filter_func) in handlers.items():
        handler = RotatingFileHandler(
            f"logs/{component}/{level}.log", maxBytes=1_048_576, backupCount=3
        )
        handler.setLevel(log_level)
        handler.addFilter(filter_func)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
