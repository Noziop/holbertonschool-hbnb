# app/api/utils.py
"""Spooky API utilities for our haunted endpoints! 👻"""

import logging
from functools import wraps

from flask import request


def api_logger(func):
    """A ghostly decorator to track API calls! 👻

    Wraps API endpoints with supernatural logging powers:
    * Captures the spirit of each request
    * Tracks successful hauntings
    * Records paranormal activities
    * Documents spectral failures
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("hbnb_api")
        resource = args[0].__class__.__name__
        method = func.__name__
        endpoint = request.endpoint

        logger.debug(
            f"🎃 {method.upper()} request to {endpoint}"
            f"\n👻 Resource: {resource}"
            f"\n📦 Parameters: {kwargs}"
        )

        try:
            result = func(*args, **kwargs)
            logger.info(
                f"✨ {resource}.{method} successfully channeled the spirits"
            )
            return result
        except Exception as e:
            logger.error(f"💀 {resource}.{method} failed: {str(e)}")
            raise

    return wrapper
