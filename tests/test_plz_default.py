from __future__ import annotations

from unittest.mock import Mock

import pytest

from pyplz import plz
from pyplz.command import Command
from tests.conftest import TestUtils


class TestPlzDefault:
    @TestUtils.patch_method(plz.list_tasks)
    def test_default_behavior(self, mock_list_tasks):
        plz._main_execute(Command())
        mock_list_tasks.assert_called_once()

    def test_default_custom_task(self):
        mock_func = Mock()

        @plz.task(default=True)
        def sample_task():
            mock_func()

        cmd = Command()
        plz._main_execute(cmd)

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
            cmd = Command()
            plz._main_execute(cmd)
