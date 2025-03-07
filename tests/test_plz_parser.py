from unittest.mock import Mock

import pytest

from pyplz import plz
from pyplz.exceptions import TaskNotFoundError
from pyplz.plz_parser import PlzParser


class TestPlzParser:
    def test_plz_parser_task_with_args_task_parser_called(self):
        @plz.task()
        def sample_task(some_bool: bool):
            pass

        task_parser_mock = Mock()
        task_parser_mock.parse = Mock()
        parser = PlzParser(plz_app=plz, task_parser=task_parser_mock)

        parser.parse(["sample-task", "--some-bool"])

        task_parser_mock.parse.assert_called_once_with(task=plz._tasks["sample-task"], args=["--some-bool"])

    def test_plz_parser_task_without_args_task_parser_called(self):
        @plz.task()
        def sample_task(some_bool: bool):
            pass

        task_parser_mock = Mock()
        task_parser_mock.parse = Mock()
        parser = PlzParser(plz_app=plz, task_parser=task_parser_mock)

        parser.parse(["sample-task"])

        task_parser_mock.parse.assert_called_once_with(task=plz._tasks["sample-task"], args=[])

    def test_plz_parser_nonexisting_task_error_raised(self):
        task_parser_mock = Mock()
        task_parser_mock.parse = Mock()
        parser = PlzParser(plz_app=plz, task_parser=task_parser_mock)

        with pytest.raises(TaskNotFoundError) as einfo:
            parser.parse(["non_existing_task"])
            assert einfo.value.task_name == "non_existing_task"

    def test_plz_parser_empty(self):
        task_parser_mock = Mock()
        task_parser_mock.parse = Mock()
        parser = PlzParser(plz_app=plz, task_parser=task_parser_mock)

        cmd = parser.parse([])

        assert cmd.is_default()
        assert cmd.task is None
        assert cmd.task_kwargs is None
        assert cmd.list is False
        assert cmd.show_env is False
        assert cmd.show_env_all is False
