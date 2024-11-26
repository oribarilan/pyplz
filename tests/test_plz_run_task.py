from __future__ import annotations

from typing import Callable

from plz import plz
from tests.test_utils import TestUtils


class TestPlzRunTask:
    def _run_task(self, func: Callable | None, *args):
        func_name = func.__name__ if func else None
        plz._main_execute(func_name, *args)

    @TestUtils.patch_method(plz.list_tasks)
    def test_default_list_task(self, mock_list_tasks):
        self._run_task(None)
        mock_list_tasks.assert_called_once()
