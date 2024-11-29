from __future__ import annotations

from unittest.mock import Mock

from pyplz import plz
from pyplz.command import Command


class TestPlzTask:
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

        cmd = Command("sample_task")
        plz._main_execute(cmd)

        mock_func.assert_called_once()

    def test_task_with_arguments(self):
        mock_func = Mock()

        @plz.task()
        def sample_task(arg1, arg2):
            mock_func(arg1, arg2)

        cmd = Command("sample_task", _args=["arg1_value", "arg2_value"])
        plz._main_execute(cmd)

        mock_func.assert_called_once_with("arg1_value", "arg2_value")

    def test_task_with_positional_arguments(self):
        mock_func = Mock()

        @plz.task()
        def sample_task(*args):
            mock_func(*args)

        cmd = Command("sample_task", _args=["arg1_value", "arg2_value"])
        plz._main_execute(cmd)

        mock_func.assert_called_once_with("arg1_value", "arg2_value")

    def test_task_with_default_arguments(self):
        mock_func = Mock()

        @plz.task()
        def sample_task(arg1="default1", arg2="default2"):
            mock_func(arg1, arg2)

        cmd = Command("sample_task")
        plz._main_execute(cmd)

        mock_func.assert_called_once_with("default1", "default2")
