from __future__ import annotations

from unittest.mock import Mock, call


from pyplz import plz
from pyplz.command import Command


class TestPlzTaskRequires:
    def test_task_requires_single(self):
        mock_parent = Mock()
        mock_parent.required, mock_parent.requires = Mock(), Mock()

        @plz.task()
        def required():
            mock_parent.required()

        @plz.task(requires=required)
        def requires():
            mock_parent.requires()

        cmd = Command("requires")
        plz._main_execute(cmd)

        # Assert the order of calls
        mock_parent.assert_has_calls([call.required(), call.requires()])

    def test_task_requires_single_with_args(self):
        mock_parent = Mock()
        mock_parent.required, mock_parent.requires = Mock(), Mock()

        @plz.task()
        def required(arg1, arg2):
            mock_parent.required(arg1, arg2)

        @plz.task(requires=[(required, ("arg1_value", "arg2_value"))])
        def requires():
            mock_parent.requires()

        cmd = Command("requires")
        plz._main_execute(cmd)

        # Assert the order of calls
        mock_parent.assert_has_calls([call.required("arg1_value", "arg2_value"), call.requires()])

    def test_task_requires_multiple_with_args(self):
        mock_parent = Mock()
        mock_parent.required1, mock_parent.required1, mock_parent.requires = Mock(), Mock(), Mock()

        @plz.task()
        def required1(arg1, arg2):
            mock_parent.required1(arg1, arg2)

        @plz.task()
        def required2(arg1, arg2):
            mock_parent.required2(arg1, arg2)

        @plz.task(requires=[(required1, ("req1_arg1_v", "req1_arg2_v")), (required2, ("req2_arg1_v", "req2_arg2_v"))])
        def requires():
            mock_parent.requires()

        cmd = Command("requires")
        plz._main_execute(cmd)

        # Assert the order of calls
        mock_parent.assert_has_calls(
            [
                call.required1("req1_arg1_v", "req1_arg2_v"),
                call.required2("req2_arg1_v", "req2_arg2_v"),
                call.requires(),
            ]
        )

    def test_task_requires_multiple(self):
        mock_parent = Mock()
        mock_parent.required1, mock_parent.required1, mock_parent.requires = Mock(), Mock(), Mock()

        @plz.task()
        def required1():
            mock_parent.required1()

        @plz.task()
        def required2():
            mock_parent.required2()

        @plz.task(requires=[required1, required2])
        def requires():
            mock_parent.requires()

        cmd = Command("requires")
        plz._main_execute(cmd)

        # Assert the order of calls
        mock_parent.assert_has_calls(
            [
                call.required1(),
                call.required2(),
                call.requires(),
            ]
        )

    def test_task_requires_chain_dep(self):
        mock_parent = Mock()
        mock_parent.required1, mock_parent.required1, mock_parent.requires = Mock(), Mock(), Mock()

        @plz.task()
        def required1():
            mock_parent.required1()

        @plz.task(requires=required1)
        def required2():
            mock_parent.required2()

        @plz.task(requires=[required1, required2])
        def requires():
            mock_parent.requires()

        cmd = Command("requires")
        plz._main_execute(cmd)

        # Assert the order of calls
        mock_parent.assert_has_calls(
            [
                call.required1(),
                call.required1(),
                call.required2(),
                call.requires(),
            ]
        )
