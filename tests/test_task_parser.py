from typing import Optional
from unittest.mock import Mock

import pytest

from pyplz import plz
from pyplz.exceptions import ForwardRefrenceNotSupported
from pyplz.task_parser import TaskParser


class TestTaskParser:
    def test_task_parser_kwargs_single(self):
        @plz.task()
        def sample_task(some_bool: bool):
            pass

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        cmd = parser.parse(task=task, args=["--some-bool"])

        assert cmd.task == task
        assert cmd.task_kwargs == {"some_bool": True}

    def test_task_parser_kwargs_default_true(self):
        @plz.task()
        def sample_task(some_bool: bool = True):
            pass

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        cmd = parser.parse(task=task, args=["--some-bool"])

        assert cmd.task == task
        assert cmd.task_kwargs == {"some_bool": False}

    def test_task_parser_kwargs_multi(self):
        impl_mock = Mock()

        @plz.task()
        def sample_task(some_bool: bool, some_int: int):
            impl_mock(some_bool=some_bool, some_int=some_int)

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        cmd = parser.parse(task=task, args=["--some-bool", "--some-int", "42"])

        assert cmd.task == task
        assert cmd.task_kwargs == {"some_bool": True, "some_int": 42}

    def test_task_parser_vanilla(self):
        impl_mock = Mock()

        @plz.task()
        def sample_task():
            impl_mock()

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        cmd = parser.parse(task=task, args=[])

        assert cmd.task == task
        assert cmd.task_kwargs == {}

    def test_task_parser_vanilla_missing_args(self, capfd):
        @plz.task()
        def sample_task(some_int: int):
            pass

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        with pytest.raises(SystemExit) as exc_info:
            parser.parse(task=task, args=[])

        assert exc_info.value.code == 2  # argparse exits with code 2 on error

        # Capture the output
        captured = capfd.readouterr()
        assert "the following arguments are required: --some-int" in captured.err

    def test_task_parser_vanilla_missing_args_but_has_default(self, capfd):
        @plz.task()
        def sample_task(some_int: int = 10):
            pass

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        cmd = parser.parse(task=task, args=[])

        assert cmd.task == task
        assert cmd.task_kwargs == {"some_int": 10}

    def test_task_parser_vanilla_missing_args_but_nullable(self, capfd):
        @plz.task()
        def sample_task(some_int: Optional[int]):
            pass

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        cmd = parser.parse(task=task, args=[])

        assert cmd.task == task
        assert cmd.task_kwargs == {"some_int": None}

    def test_task_parser_forward_ref_causes_error(self, capfd):
        @plz.task()
        def sample_task(some_int: "int"):
            pass

        task = plz._tasks["sample-task"]
        parser = TaskParser()

        with pytest.raises(ForwardRefrenceNotSupported):
            parser.parse(task=task, args=[])
