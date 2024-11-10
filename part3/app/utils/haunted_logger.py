"""Spooky spells module for our haunted logging system! 👻"""

import logging
import os
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import g, request


class HauntedLogger:
    """Notre système de logging hanté amélioré ! 👻"""

    LOG_LEVELS = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "ERROR": logging.ERROR,
    }

    def __init__(self):
        self.setup_logging()

    def setup_logging(self):
        """Initialisation du système de logging."""
        # Nettoyage des handlers existants
        for logger in logging.root.manager.loggerDict.values():
            if isinstance(logger, logging.Logger):
                logger.handlers = []

        # Configuration de base
        logging.basicConfig(level=logging.DEBUG)
        
        # Configuration des loggers par composant
        self.loggers = {}
        for component in ["api", "business", "persistence"]:
            self.loggers[component] = self._setup_component_logger(component)

    def _setup_component_logger(self, component: str):
        """Setup un logger spécifique pour chaque composant."""
        logger = logging.getLogger(f"hbnb.{component}")
        logger.setLevel(logging.DEBUG)
        logger.propagate = False  # Évite la duplication

        # Format commun
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(function_name)s | %(module_name)s | "
            "%(user_id)s | %(request_id)s | %(message)s"
        )

        # Classe de filtre par niveau
        class LevelFilter(logging.Filter):
            def __init__(self, level):
                self.level = level
                
            def filter(self, record):
                return record.levelno == self.level

        # Création des dossiers si nécessaire
        log_dir = Path(f"logs/{component}")
        log_dir.mkdir(parents=True, exist_ok=True)

        # Configuration des handlers par niveau
        handlers = {
            'DEBUG': (logging.DEBUG, log_dir / "debug.log"),
            'INFO': (logging.INFO, log_dir / "info.log"),
            'ERROR': (logging.ERROR, log_dir / "error.log")
        }

        for level_name, (level, filepath) in handlers.items():
            handler = RotatingFileHandler(
                filepath,
                maxBytes=1_048_576,
                backupCount=5
            )
            handler.setFormatter(formatter)
            handler.addFilter(LevelFilter(level))  # Filtre strict par niveau
            handler.setLevel(level)
            logger.addHandler(handler)

        return logger

    def log_me(self, component="api"):
        """Décorateur de logging amélioré."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                logger = self.loggers[component]
                
                # Contexte enrichi
                extra = {
                    "function_name": func.__name__,
                    "module_name": func.__module__,
                    "user_id": getattr(g, 'user_id', 'anonymous'),
                    "request_id": getattr(g, 'request_id', '-'),
                    "call_args": str(args),
                    "call_kwargs": str(kwargs)
                }

                try:
                    logger.debug(
                        f"🎭 Starting {func.__name__} | Args: {extra['call_args']} | Kwargs: {extra['call_kwargs']}",
                        extra=extra
                    )
                    
                    result = func(*args, **kwargs)
                    
                    logger.info(
                        f"✨ {func.__name__} completed | Result type: {type(result)}",
                        extra=extra
                    )
                    return result
                    
                except Exception as e:
                    logger.error(
                        f"💀 Error in {func.__name__}: {str(e)} | Args: {extra['call_args']}",
                        exc_info=True,
                        extra=extra
                    )
                    raise
            return wrapper
        return decorator


# Créer une instance globale
haunted_logger = HauntedLogger()
log_me = haunted_logger.log_me
