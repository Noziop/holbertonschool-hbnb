"""Spooky spells module for our haunted logging system! 👻"""
import logging
from pathlib import Path

def setup_logging():
    """Initialize our haunted logging system! 🎭
    
    Sets up logging configuration with file handlers for each logger type.
    Creates necessary log directories if they don't exist.
    """
    # Create log directories if they don't exist
    for log_type in ['api', 'models', 'validation']:
        log_path = Path(f'logs/{log_type}/debug.log')
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.touch()

        # Create and configure logger
        logger_name = f'hbnb_{log_type}'
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)

        # Create and configure file handler
        handler = logging.FileHandler(str(log_path))
        handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        logger.addHandler(handler)