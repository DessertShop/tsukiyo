from functools import wraps
from typing import Dict, Callable


def singleton(class_: Callable) -> Callable:
    """Singleton decorator"""
    instances: Dict = {}

    @wraps(class_)
    def wrapper(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return wrapper
