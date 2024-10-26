"""Spooky spells module for our haunted logging system! 👻"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging():
    """Initialize our haunted logging system! 🎭
    
    Sets up logging configuration with rotating file handlers.
    Creates necessary log directories if they don't exist.
    """
    # Max size 1MB, keep 3 backup files
    MAX_BYTES = 1_048_576  # 1MB in bytes
    BACKUP_COUNT = 3

    # Create log directories if they don't exist
    for log_type in ['api', 'models', 'validation']:
        for level in ['debug', 'info', 'error']:
            log_path = Path(f'logs/{log_type}/{level}.log')
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.touch()

        # Create and configure logger
        logger_name = f'hbnb_{log_type}'
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Create and configure rotating handlers for each level
        debug_handler = RotatingFileHandler(
            f'logs/{log_type}/debug.log',
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT
        )
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)

        info_handler = RotatingFileHandler(
            f'logs/{log_type}/info.log',
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT
        )
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        error_handler = RotatingFileHandler(
            f'logs/{log_type}/error.log',
            maxBytes=MAX_BYTES,
            backupCount=BACKUP_COUNT
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        # Remove existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Add handlers to logger
        logger.addHandler(debug_handler)
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)