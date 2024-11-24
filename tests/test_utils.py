from typing import Callable
from unittest.mock import patch


class TestUtils:
    @staticmethod
    def patch_method(func: Callable) -> Callable:
        return patch(f"{func.__module__}.{func.__qualname__}")
