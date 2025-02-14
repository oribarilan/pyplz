from __future__ import annotations

from unittest.mock import Mock

from pyplz import plz
from pyplz.command import Command
from pyplz.task import Task


class TestPlzHelp:
    def test_help_global(self):
        cmd = Command(help=True)
        print_help_mock = Mock()
        plz._print_help = print_help_mock

        plz._main_execute(cmd)

        print_help_mock.assert_called_once()

    def test_help_task(self):
        print_help_mock = Mock()
        sample_task_mock = Mock()
        Task.print_help = print_help_mock

        @plz.task()
        def sample_task():
            sample_task_mock()

        cmd = Command(task="sample_task", help=True)

        plz._main_execute(cmd)

        print_help_mock.assert_called_once()
        sample_task_mock.assert_not_called()
