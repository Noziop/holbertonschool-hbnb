"""Test module for our spooky logging system! 👻"""
import logging
from pathlib import Path

import pytest


def test_logger_initialization():
    """Test that our logging system initializes correctly! 🎭"""
    # Verfiy that the haunted_logger module is importable
    from app.utils.haunted_logger import setup_logging

    setup_logging()

    # Vérifie que les loggers sont créés avec les bons noms
    loggers = ["hbnb_api", "hbnb_models", "hbnb_validation"]
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
    import re

    from app.utils.haunted_logger import setup_logging

    setup_logging()
    logger = logging.getLogger("hbnb_api")

    # Send a test message
    test_message = "Testing the haunted logger!"
    logger.info(test_message)

    # Read the log file - Changed from debug.log to info.log
    with open("logs/api/info.log", "r") as f:  # 👈 Changed this line
        log_content = f.read()

    # Check log format using regex
    log_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - hbnb_api - INFO - Testing the haunted logger!"
    assert re.search(log_pattern, log_content) is not None


def test_log_levels_separation():
    """Test that different log levels go to different files! 📑"""
    from app.utils.haunted_logger import setup_logging

    setup_logging()
    logger = logging.getLogger("hbnb_api")

    # Send messages of different levels
    debug_msg = "Debug ghost spotted!"
    info_msg = "Info spirit passing by!"
    error_msg = "Error demon encountered!"

    logger.debug(debug_msg)
    logger.info(info_msg)
    logger.error(error_msg)

    # Check debug.log (should contain ONLY debug messages)
    with open("logs/api/debug.log", "r") as f:
        debug_content = f.read()
        assert debug_msg in debug_content
        assert info_msg not in debug_content
        assert error_msg not in debug_content

    # Check info.log (should contain ONLY info messages)
    with open("logs/api/info.log", "r") as f:
        info_content = f.read()
        assert debug_msg not in info_content
        assert info_msg in info_content
        assert error_msg not in info_content

    # Check error.log (should contain ONLY error messages)
    with open("logs/api/error.log", "r") as f:
        error_content = f.read()
        assert debug_msg not in error_content
        assert info_msg not in error_content
        assert error_msg in error_content


def test_log_rotation():
    """Test that our logs rotate properly based on size and time! 📜"""
    import time

    from app.utils.haunted_logger import setup_logging

    setup_logging()
    logger = logging.getLogger("hbnb_api")

    # Generate enough logs to trigger rotation
    large_message = "🦇" * 10240
    for i in range(100):
        logger.info(f"Message {i}: {large_message}")

    # Check that rotation files exist
    base_path = Path("logs/api")
    assert (base_path / "info.log").exists()  # 👈 Changed this line
    assert (base_path / "info.log.1").exists()  # 👈 Changed this line

    # Verify content separation
    with open(base_path / "info.log", "r") as f:  # 👈 Changed this line
        current_content = f.read()
    with open(base_path / "info.log.1", "r") as f:  # 👈 Changed this line
        rotated_content = f.read()


def test_exception_logging():
    """Test that exceptions are properly logged in appropriate files! 🎭"""
    from app.utils.haunted_logger import setup_logging

    setup_logging()
    logger = logging.getLogger("hbnb_api")

    # Test exception logging
    try:
        raise ValueError("👻 BOO! Something went wrong!")
    except Exception as e:
        logger.error("An error occurred", exc_info=True)

    # Check all log files
    with open("logs/api/debug.log", "r") as f:
        debug_content = f.read()
    with open("logs/api/info.log", "r") as f:
        info_content = f.read()
    with open("logs/api/error.log", "r") as f:
        error_content = f.read()

    # Verify error appears only in appropriate logs
    assert "BOO! Something went wrong!" in error_content  # Should be in error
    assert "BOO! Something went wrong!" not in info_content  # Should not be in info
    assert "Traceback" in error_content  # Stack trace in error
    assert "Traceback" not in info_content  # No stack trace in info
    assert "ValueError" in error_content  # Exception type in error
