import logging, json, traceback, socket, os
from functools import wraps
from datetime import datetime, timezone



def magic_wand(*wrappers):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for wrap in wrappers:
                result = wrap(*args, **kwargs)
                if result is False:
                    return
            return func(*args, **kwargs)
        return wrapper
    return decorator

def validate_entity(get_entity_func):
    def wrapper(*args, **kwargs):
        if not get_entity_func(*args, **kwargs):
            raise ValueError(f"Entity does not exist")
        return True
    return wrapper

def validate_input(**validators):
    def wrapper(*args, **kwargs):
        for param, validator in validators.items():
            if param in kwargs:
                kwargs[param] = validator(kwargs[param])
        return True
    return wrapper

def error_handler(*args, **kwargs):
    try:
        return True
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")

def update_timestamp(*args, **kwargs):
    self = args[0] if args else None
    if self:
        self.updated_at = datetime.now(timezone.utc)
    return True

def to_dict(exclude=[]):
    def wrapper(self):
        result = self.__dict__.copy()
        return {k: v for k, v in result.items() if k not in exclude}
    return wrapper

def validate_types(**type_checks):
    def wrapper(*args, **kwargs):
        for param, expected_type in type_checks.items():
            if param in kwargs and not isinstance(kwargs[param], expected_type):
                raise TypeError(f"{param} must be of type {expected_type}")
        return True
    return wrapper

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

# Wrapper de logging amélioré
def log_action(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        class_name = args[0].__class__.__name__ if args else ''
        
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'class': class_name,
            'method': func_name,
            'args': str(args[1:]),
            'kwargs': {k: v for k, v in kwargs.items() if k != 'password'},
            'hostname': socket.gethostname(),
            'process_id': os.getpid(),
            'thread_id': threading.get_ident()
        }
        
        if 'user_id' in kwargs:
            log_data['user_id'] = kwargs['user_id']
        if 'session_id' in kwargs:
            log_data['session_id'] = kwargs['session_id']
        
        logger.debug(json.dumps(log_data))
        
        try:
            result = func(*args, **kwargs)
            log_data['status'] = 'success'
            if isinstance(result, dict):
                log_data['result_summary'] = {k: v for k, v in result.items() if k != 'password'}
            logger.info(json.dumps(log_data))
            return result
        except ValueError as e:
            log_data['status'] = 'value_error'
            log_data['error_message'] = str(e)
            log_data['traceback'] = traceback.format_exc()
            logger.warning(json.dumps(log_data))
            raise
        except Exception as e:
            log_data['status'] = 'error'
            log_data['error_message'] = str(e)
            log_data['traceback'] = traceback.format_exc()
            logger.error(json.dumps(log_data))
            raise
    return wrapper

