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

    def test_task_to_string(self):
        def sample_task():
            pass

        task = Task(sample_task)

        assert str(task) == "sample_task"

    def test_task_to_string_default(self):
        def sample_task():
            pass

        task = Task(sample_task, is_default=True)

        assert str(task) == "sample_task [default]"

    def test_task_to_string_builtin(self):
        def sample_task():
            pass

        task = Task(sample_task, is_builtin=True)

        assert str(task) == "sample_task [builtin]"

    def test_task_to_string_default_builtin(self):
        def sample_task():
            pass

        task = Task(sample_task, is_default=True, is_builtin=True)

        assert str(task) == "sample_task [default] [builtin]"
