import sys
from unittest.mock import Mock

import pytest

from pyplz import plz
from pyplz.main import main


class TestMain:
    def test_main_task(self):
        impl_mock = Mock()

        @plz.task()
        def sample_task():
            impl_mock()

        sys.argv = ["plz", "sample-task"]

        main()

        impl_mock.assert_called_once()

    def test_main_nonexisting_task(self):
        impl_mock = Mock()

        @plz.task()
        def sample_task():
            impl_mock()

        sys.argv = ["plz", "nonexisting_task"]

        with pytest.raises(SystemExit):
            main()

    def test_main_task_with_missing_argument(self):
        impl_mock = Mock()

        @plz.task()
        def sample_task(some_bool: bool, some_int: int):
            impl_mock()

        sys.argv = ["plz", "sample-task", "--some-bool"]

        with pytest.raises(SystemExit):
            main()
