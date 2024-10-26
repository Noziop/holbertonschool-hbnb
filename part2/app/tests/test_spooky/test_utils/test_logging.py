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

def test_log_levels_separation():
    """Test that different log levels go to different files! 📑"""
    from app.utils.spooky_spells import setup_logging
    
    setup_logging()
    logger = logging.getLogger('hbnb_api')
    
    # Send messages of different levels
    debug_msg = "Debug ghost spotted!"
    info_msg = "Info spirit passing by!"
    error_msg = "Error demon encountered!"
    
    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.error(error_msg)
    
    # Check debug.log (should contain all messages)
    with open('logs/api/debug.log', 'r') as f:
        debug_content = f.read()
        assert debug_msg in debug_content
        assert info_msg in debug_content
        assert error_msg in debug_content
    
    # Check info.log (should contain info and error)
    with open('logs/api/info.log', 'r') as f:
        info_content = f.read()
        assert debug_msg not in info_content
        assert info_msg in info_content
        assert error_msg in info_content
    
    # Check error.log (should contain only error)
    with open('logs/api/error.log', 'r') as f:
        error_content = f.read()
        assert debug_msg not in error_content
        assert info_msg not in error_content
        assert error_msg in error_content

def test_log_rotation():
    """Test that our logs rotate properly based on size and time! 📜"""
    from app.utils.spooky_spells import setup_logging
    import time
    
    setup_logging()
    logger = logging.getLogger('hbnb_api')
    
    # Generate enough logs to trigger rotation (10KB per message, 100 messages)
    large_message = "🦇" * 10240  # 10KB of ghost emojis!
    for i in range(100):  # Should definitely create multiple log files
        logger.info(f"Message {i}: {large_message}")
    
    # Check that rotation files exist
    base_path = Path('logs/api')
    assert (base_path / 'debug.log').exists()
    assert (base_path / 'debug.log.1').exists()
    
    # Verify content separation
    with open(base_path / 'debug.log', 'r') as f:
        current_content = f.read()
    with open(base_path / 'debug.log.1', 'r') as f:
        rotated_content = f.read()
        
    # Messages should be different in each file
    assert current_content != rotated_content
    assert '🦇' in current_content
    assert '🦇' in rotated_content

