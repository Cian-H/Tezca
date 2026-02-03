"""Utility functions for execution control.

This module contains helper decorators and utilities, primarily focused on
managing function re-entry and recursion safety.
"""

import threading
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def recursion_guard[**P, R](
    default_return: R | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R | None]]:
    """Prevents a function from recursively calling itself within the same thread.

    This decorator uses thread-local storage to track if the decorated function
    is currently executing. If a re-entrant call is detected within the same
    execution context, the function immediately returns a default value instead
    of executing the function body again.

    This is particularly useful for avoiding infinite recursion in methods like
    `__repr__` or during complex cyclic graph traversals.

    Args:
        default_return: The value to return if recursion is detected.
            Defaults to None.

    Returns:
        A decorator function that applies the recursion guard to the target
        callable.
    """
    local_data = threading.local()

    def decorator(f: Callable[P, R]) -> Callable[P, R | None]:
        lock_name = f"{repr(f)}_lock"

        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            if getattr(local_data, lock_name, False):
                return default_return
            setattr(local_data, lock_name, True)
            try:
                return f(*args, **kwargs)
            finally:
                setattr(local_data, lock_name, False)

        return wrapper

    return decorator
