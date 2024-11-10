"""Spooky spells module for our haunted logging system! 👻"""

import logging
import os
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import g, request


class HauntedLogger:
    """Our magical logging system! 🎭"""

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "ERROR": logging.ERROR,
    }

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Initialize our haunted logging system! 🎭"""
        # Créer la structure des dossiers
        log_root = Path("logs")
        for component in ["api", "business", "persistence"]:
            for level in self.LOG_LEVELS.keys():
                log_path = log_root / component / f"{level.lower()}.log"
                log_path.parent.mkdir(parents=True, exist_ok=True)
                log_path.touch()

        # Configuration de base
        logging.basicConfig(level=logging.DEBUG)

        # Setup des loggers par composant
        self.loggers = {
            comp: self._setup_component_logger(comp)
            for comp in ["api", "business", "persistence"]
        }

    def _setup_component_logger(self, component: str):
        """Setup un logger spécifique pour chaque composant"""
        logger = logging.getLogger(f"hbnb.{component}")
        logger.setLevel(logging.DEBUG)

        # Format détaillé pour chaque log
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(function_name)s | %(module_name)s | "
            "%(message)s"
        )

        # Un handler par niveau de log
        for level_name, level in self.LOG_LEVELS.items():
            handler = RotatingFileHandler(
                f"logs/{component}/{level_name.lower()}.log",
                maxBytes=1_048_576,  # 1MB
                backupCount=5,
            )
            handler.setLevel(level)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def log_me(self, component="api"):
        """Décorateur magique pour logger les appels de fonction! ✨"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger = self.loggers[component]

                # Context de la requête
                extra = {
                    "function_name": func.__name__,
                    "module_name": func.__module__,
                    "args_info": str(args),
                    "kwargs_info": str(kwargs),
                }

                try:
                    # Log début d'appel
                    logger.debug(f"🎭 Starting {func.__name__}", extra=extra)

                    result = func(*args, **kwargs)

                    # Log succès
                    logger.info(
                        f"✨ {func.__name__} completed successfully",
                        extra=extra,
                    )
                    return result

                except Exception as e:
                    # Log erreur détaillé
                    logger.error(
                        f"💀 Error in {func.__name__}: {str(e)}",
                        exc_info=True,
                        extra=extra,
                    )
                    raise

            return wrapper

        return decorator


# Créer une instance globale
haunted_logger = HauntedLogger()
log_me = haunted_logger.log_me
