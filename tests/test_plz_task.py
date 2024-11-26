from __future__ import annotations

from typing import Callable
from unittest.mock import Mock

import pytest

from plz import plz


class TestPlzTask:
    def _run_task(self, func: Callable | None, *args):
        func_name = func.__name__ if func else None
        plz._main_execute(func_name, *args)

    # region wrapped functions for pure functionality

    def test_wrapped_func_without_arguments(self):
        @plz.task()
        def sample_task():
            return "Task executed"

        result = sample_task()
        assert result == "Task executed"

    def test_wrapped_func_with_arguments(self):
        @plz.task()
        def sample_task(arg1, arg2):
            return f"Task executed with {arg1} and {arg2}"

        result = sample_task("arg1_value", "arg2_value")
        assert result == "Task executed with arg1_value and arg2_value"

    def test_wrapped_func_with_default_arguments(self):
        @plz.task()
        def sample_task(arg1="default1", arg2="default2"):
            return f"Task executed with {arg1} and {arg2}"

        result = sample_task()
        assert result == "Task executed with default1 and default2"

    # endregion

    def test_task_without_arguments(self):
        mock_func = Mock()

        @plz.task()
        def sample_task():
            mock_func()

        self._run_task(sample_task)
        mock_func.assert_called_once()

    def test_task_with_arguments(self):
        mock_func = Mock()

        @plz.task()
        def sample_task(arg1, arg2):
            mock_func(arg1, arg2)

        self._run_task(sample_task, "arg1_value", "arg2_value")
        mock_func.assert_called_once_with("arg1_value", "arg2_value")

    def test_task_with_default_arguments(self):
        mock_func = Mock()

        @plz.task()
        def sample_task(arg1="default1", arg2="default2"):
            mock_func(arg1, arg2)

        self._run_task(sample_task)
        mock_func.assert_called_once_with("default1", "default2")

    def test_default_custom_task(self):
        mock_func = Mock()

        @plz.task(default=True)
        def sample_task():
            mock_func()

        self._run_task(None)
        mock_func.assert_called_once()

    def test_multiple_default_tasks_error(self):
        mock_func = Mock()

        @plz.task(default=True)
        def sample_task_1():
            mock_func()

        @plz.task(default=True)
        def sample_task_2():
            mock_func()

        with pytest.raises(SystemExit):
            # multiple defaults should raise an error
            self._run_task(None)
