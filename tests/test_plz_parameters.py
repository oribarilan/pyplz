from __future__ import annotations

import subprocess
from unittest.mock import Mock

import pytest

from pyplz import plz
from pyplz.command import Command


class TestPlzRun:
    def test_task_param(self):
        mock = Mock()

        @plz.task()
        def sample_task(param1: str):
            mock(param1)

        plz._main_execute(Command("sample_task", _args=["value1"]))

        mock.assert_called_once_with("value1")
