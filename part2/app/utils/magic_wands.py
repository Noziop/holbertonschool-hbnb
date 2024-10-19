# magic_wands.py
import logging, json
from functools import wraps
from datetime import datetime, timezone

def validate_entity_exists(get_entity_func):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Appel de get_entity_func au moment de l'exécution
            if not get_entity_func(self, *args, **kwargs):
                raise ValueError(f"Entity does not exist")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def validate_input(**validators):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for param, validator in validators.items():
                if param in kwargs:
                    kwargs[param] = validator(kwargs[param])
            return func(*args, **kwargs)
        return wrapper
    return decorator

def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Error in {func.__name__}: {str(e)}")
    return wrapper

def update_timestamp(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.updated_at = datetime.now(timezone.utc)
        return result
    return wrapper

def to_dict_decorator(exclude=[]):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            result = func(self)
            return {k: v for k, v in result.items() if k not in exclude}
        return wrapper
    return decorator

def validate_types(**type_checks):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for param, expected_type in type_checks.items():
                if param in kwargs:
                    if not isinstance(kwargs[param], expected_type):
                        raise TypeError(f"{param} must be of type {expected_type}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

import logging
from functools import wraps

# Configuration du logging
def setup_logging(log_file_prefix='hbnb'):
    logger = logging.getLogger('hbnb_logger')
    logger.setLevel(logging.DEBUG)

    handlers = {
        'info': logging.FileHandler(f'{log_file_prefix}_info.log'),
        'debug': logging.FileHandler(f'{log_file_prefix}_debug.log'),
        'error': logging.FileHandler(f'{log_file_prefix}_error.log')
    }

    handlers['info'].setLevel(logging.INFO)
    handlers['debug'].setLevel(logging.DEBUG)
    handlers['error'].setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    for handler in handlers.values():
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Initialisation du logger
logger = setup_logging()

# Décorateur de logging amélioré
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        class_name = args[0].__class__.__name__ if args else ''
        
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "class": class_name,
            "method": func_name,
            "args": str(args[1:]),
            "kwargs": {k: v for k, v in kwargs.items() if k != 'password'}  # Exclure le mot de passe des logs
        }
        
        # Ajout d'informations contextuelles si disponibles
        if 'user_id' in kwargs:
            log_data['user_id'] = kwargs['user_id']
        if 'session_id' in kwargs:
            log_data['session_id'] = kwargs['session_id']
        
        logger.debug(json.dumps(log_data))
        
        try:
            result = func(*args, **kwargs)
            log_data["status"] = "success"
            if isinstance(result, dict):
                log_data["result_summary"] = {k: v for k, v in result.items() if k != 'password'}
            logger.info(json.dumps(log_data))
            return result
        except ValueError as e:
            log_data["status"] = "value_error"
            log_data["error_message"] = str(e)
            logger.debug(json.dumps(log_data))
            raise
        except Exception as e:
            log_data["status"] = "error"
            log_data["error_message"] = str(e)
            logger.error(json.dumps(log_data))
            raise
    return wrapper

