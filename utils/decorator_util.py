from functools import wraps
from threading import Lock


def singleton(cls):
    instance = None
    lock = Lock()
    @wraps(cls)
    def wrapper(*args, **kwargs):
        nonlocal instance
        if instance is None:
            with lock:
                if instance is None:
                    instance = cls(*args, **kwargs)
        return instance

    return wrapper

