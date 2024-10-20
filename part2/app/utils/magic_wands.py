import logging, json, os
from datetime import datetime, timezone
from functools import wraps
from .model_validations import *


# Création du répertoire pour les logs
log_directory = 'app/logs'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configuration du logging
def setup_logging():
    logger = logging.getLogger('hbnb_logger')
    logger.setLevel(logging.DEBUG)

    # Handler pour les logs de debug
    debug_handler = logging.FileHandler(f'{log_directory}/debug.log')
    debug_handler.setLevel(logging.DEBUG)

    # Handler pour les logs d'info
    info_handler = logging.FileHandler(f'{log_directory}/info.log')
    info_handler.setLevel(logging.INFO)

    # Handler pour les logs d'erreur
    error_handler = logging.FileHandler(f'{log_directory}/error.log')
    error_handler.setLevel(logging.ERROR)

    # Formateur pour les logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    debug_handler.setFormatter(formatter)
    info_handler.setFormatter(formatter)
    error_handler.setFormatter(formatter)

    # Ajout des handlers au logger
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(error_handler)

    return logger

# Initialisation du logger
logger = setup_logging()
print("Logger initialized")

def magic_wand(*wrappers):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            log_data = _prepare_log_data(func, args, kwargs)
            try:
                for wrap in sorted(wrappers, key=lambda w: getattr(w, 'priority', 0), reverse=True):
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

def validate_entity(model_name, id_field):
    def wrapper(*args, **kwargs):
        if id_field in kwargs:
            # Import dynamique du modèle
            import importlib
            module = importlib.import_module(f'app.models.{model_name.lower()}')
            model_class = getattr(module, model_name)
            entity = model_class.get_by_id(kwargs[id_field])
            if not entity:
                raise ValueError(f"{model_name} with id {kwargs[id_field]} does not exist")
        return True
    wrapper.priority = 1
    return wrapper

def validate_input(*args, **kwargs):
    if args:
        # Si des arguments positionnels sont fournis, on suppose que c'est un seul dictionnaire
        validators = args[0]
    else:
        # Sinon, on utilise les arguments nommés
        validators = kwargs

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
    wrapper.priority = 2
    return wrapper

def _prepare_log_data(func, args, kwargs):
    return {
        'function': func.__name__,
        'class': args[0].__class__.__name__ if args else '',
        'args': str(args[1:]),
        'kwargs': {k: v for k, v in kwargs.items() if k != 'password'}
    }

def update_timestamp(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        self.updated_at = datetime.now(timezone.utc)
        return result
    wrapper.priority = 3  # Ajuste la priorité selon tes besoins
    return wrapper

def to_dict(exclude=[]):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            result = func(self)
            return {k: v for k, v in result.items() if k not in exclude}
        wrapper.priority = 5  # Ajout de la priorité
        return wrapper
    return decorator