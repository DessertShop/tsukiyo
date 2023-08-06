from functools import wraps
from typing import Dict, Callable, TypeVar, cast

T = TypeVar("T")


def singleton(class_: Callable[..., T]) -> Callable[..., T]:
    """Singleton decorator"""
    instances: Dict = {}

    @wraps(class_)
    def wrapper(*args, **kwargs) -> T:
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return cast(T, instances[class_])

    return wrapper
