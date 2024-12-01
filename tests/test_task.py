import pytest
from pyplz.task import Task


class TestTask:
    def test_task_desc_multiline(self):
        def test_task():
            """
            This is a test task
            that spans multiple lines.
            Let's see if it works.
            """
            pass

        task = Task(test_task)

        assert task.desc == "This is a test task\nthat spans multiple lines.\nLet's see if it works."

    def test_task_desc(self):
        def test_task():
            """This is a test task"""
            pass

        task = Task(test_task)

        assert task.desc == "This is a test task"

    def test_task_requires_normalized(self):
        def test_task():
            pass

        task = Task(test_task, requires=None)

        assert task.requires == []

    def test_task_called_with_missing_args(self):
        def test_task(arg1, arg2):
            pass

        task = Task(test_task)

        with pytest.raises(SystemExit):
            task("arg1")
