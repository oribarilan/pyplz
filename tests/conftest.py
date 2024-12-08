from typing import Callable
from unittest.mock import patch

import pytest

from pyplz import plz


@pytest.fixture(scope="session", autouse=True)
def clear_plz():
    with patch("pyplz.plz._load_plzfile") as mock_load_plzfile:
        mock_load_plzfile.return_value = None
        yield


@pytest.fixture(scope="function", autouse=True)
def reset_plz():
    plz._reset()


class TestUtils:
    @staticmethod
    def patch_method(func: Callable) -> Callable:
        return patch(f"{func.__module__}.{func.__qualname__}")
