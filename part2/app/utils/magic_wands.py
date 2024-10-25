import logging
import json
import os
from datetime import datetime, timezone
from functools import wraps
from logging.handlers import RotatingFileHandler
from .model_validations import *

class EntityNotFoundError(Exception):
    """Raised when an entity is not found in the database 👻"""
    pass

# Création du répertoire pour les logs
log_directory = 'app/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration du logging
def setup_logging():
    loggers = {}
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    for module in ['models', 'facade', 'api']:
        logger = logging.getLogger(f'hbnb_{module}')
        logger.setLevel(logging.DEBUG)

        # Handler pour les logs de debug
        debug_handler = RotatingFileHandler(f'{log_directory}/{module}_debug.log', maxBytes=1024*1024, backupCount=5)
        debug_handler.setLevel(logging.DEBUG)
        debug_handler.setFormatter(formatter)

        # Handler pour les logs d'info
        info_handler = RotatingFileHandler(f'{log_directory}/{module}_info.log', maxBytes=1024*1024, backupCount=5)
        info_handler.setLevel(logging.INFO)
        info_handler.setFormatter(formatter)

        # Handler pour les logs d'erreur
        error_handler = RotatingFileHandler(f'{log_directory}/{module}_error.log', maxBytes=1024*1024, backupCount=5)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)

        logger.addHandler(debug_handler)
        logger.addHandler(info_handler)
        logger.addHandler(error_handler)

        loggers[module] = logger

    return loggers

# Initialisation des loggers
loggers = setup_logging()
print("Loggers initialized")

def get_logger(module):
    return loggers.get(module, logging.getLogger('hbnb_default'))

def _prepare_log_data(func, args, kwargs):
    return {
        'function': func.__name__,
        'class': args[0].__class__.__name__ if args else '',
        'args': str(args[1:]),
        'kwargs': {k: v for k, v in kwargs.items() if k != 'password'}
    }

def magic_wand(*wrappers):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            module = func.__module__.split('.')[-2]
            logger = get_logger(module)
            log_data = _prepare_log_data(func, args, kwargs)
            try:
                for wrap in sorted(wrappers, key=lambda w: getattr(w, 'priority', 0), reverse=True):
                    if callable(wrap):
                        result = wrap(*args, **kwargs)
                        if isinstance(result, dict):
                            kwargs.update(result)
                        elif result is False:
                            logger.debug(json.dumps({**log_data, 'status': 'validation_failed', 'wrapper': wrap.__name__}))
                            return
                result = func(*args, **kwargs)
                logger.info(json.dumps({**log_data, 'status': 'success', 'result': str(result)}))
                return result
            except ValueError as e:
                logger.debug(json.dumps({**log_data, 'status': 'value_error', 'error': str(e)}))
                raise
            except Exception as e:
                logger.error(json.dumps({**log_data, 'status': 'error', 'error': str(e)}))
                raise
        return wrapper
    return decorator

def validate_entity(*args):
    entity_validations = {}
    i = 0
    while i < len(args):
        if isinstance(args[i], tuple) and len(args[i]) == 2:
            model_name, field = args[i]
            entity_validations[field] = model_name
            i += 1
        elif i + 1 < len(args) and isinstance(args[i], str) and isinstance(args[i+1], str):
            model_name, field = args[i], args[i+1]
            entity_validations[field] = model_name
            i += 2
        else:
            raise ValueError(f"Invalid arguments for validate_entity: {args[i]}")

    def wrapper(*func_args, **func_kwargs):
        for field, model_name in entity_validations.items():
            if field in func_kwargs:
                import importlib
                module = importlib.import_module(f'app.models.{model_name.lower()}')
                model_class = getattr(module, model_name)
                entity = model_class.get_by_id(func_kwargs[field])
                raise EntityNotFoundError(
                        f"{model_name} with id {func_kwargs[field]} does not exist! 👻"
                    )
        return func_args, func_kwargs
    wrapper.priority = 2
    return wrapper

def validate_input(*args, **kwargs):
    validators = {}
    for arg in args:
        if isinstance(arg, dict):
            validators.update(arg)
    validators.update(kwargs)

    def wrapper(*func_args, **func_kwargs):
        validated = {}
        for param, expected_type in validators.items():
            if param in func_kwargs:
                try:
                    value = func_kwargs[param]
                    if isinstance(expected_type, tuple):
                        if not isinstance(value, expected_type):
                            raise ValueError(f"{param} must be one of types {expected_type}")
                    elif not isinstance(value, expected_type):
                        raise ValueError(f"{param} must be of type {expected_type.__name__}")
                    validated[param] = value
                except ValueError as e:
                    raise ValueError(f"Invalid {param}: {str(e)}")
        return validated
    wrapper.priority = 1
    return wrapper

def update_timestamp(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        now = datetime.now(timezone.utc)
        result = func(self, *args, **kwargs)
        if not hasattr(self, 'updated_at') or (now - self.updated_at).total_seconds() > 1:
            self.updated_at = now
        return result
    wrapper.priority = 3
    return wrapper

def to_dict(exclude=[]):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            result = func(self)
            filtered = {k: v for k, v in result.items() 
                      if k not in ['password', 'password_hash'] 
                      and k not in exclude}
            return filtered
        wrapper.priority = 4
        return wrapper
    return decorator