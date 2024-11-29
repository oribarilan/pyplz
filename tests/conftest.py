from typing import Callable
from unittest.mock import patch

import pytest

from pyplz import plz


@pytest.fixture(autouse=True)
def patch_methods():
    plz._reset()


class TestUtils:
    @staticmethod
    def patch_method(func: Callable) -> Callable:
        return patch(f"{func.__module__}.{func.__qualname__}")
