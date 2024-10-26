"""Test module for our spooky logging system! 👻"""
import pytest
import logging
from pathlib import Path

def test_logger_initialization():
    """Test that our logging system initializes correctly! 🎭"""
    # Verfiy that the spooky_spells module is importable
    from app.utils.spooky_spells import setup_logging
    
    setup_logging()
    
    # Vérifie que les loggers sont créés avec les bons noms
    loggers = ['hbnb_api', 'hbnb_models', 'hbnb_validation']
    for name in loggers:
        logger = logging.getLogger(name)
        assert logger is not None
        assert logger.name == name
        # Vérifie que le logger a au moins un handler
        assert len(logger.handlers) > 0
        # Vérifie que les fichiers de log existent
        log_file = Path(f'logs/{name.split("_")[1]}/debug.log')
        assert log_file.exists()

def test_log_formatting():
    """Test that our logs are properly formatted! 📝"""
    from app.utils.spooky_spells import setup_logging
    import re
    
    setup_logging()
    logger = logging.getLogger('hbnb_api')
    
    # Send a test message
    test_message = "Testing the haunted logger!"
    logger.info(test_message)
    
    # Read the log file
    with open('logs/api/debug.log', 'r') as f:
        log_content = f.read()
    
    # Check log format using regex
    # Format should be: YYYY-MM-DD HH:MM:SS,mmm - logger_name - LEVEL - message
    log_pattern = r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - hbnb_api - INFO - Testing the haunted logger!'
    
    assert re.search(log_pattern, log_content) is not None

