from functools import wraps


class Log:
    def __init__(self, logger, name):
        self.logger = logger
        self.name = name

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            self.logger.info(f'{func.__name__} with args {args} and kwargs {kwargs} in {self.name}')
            return result

        return wrapper
