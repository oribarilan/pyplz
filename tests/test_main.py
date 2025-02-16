import sys
from unittest.mock import Mock

from pytest import skip
import pytest

from pyplz.command import Parser
from pyplz.main import main
from pyplz.plz_app import PlzApp
from tests.conftest import TestUtils


class TestMain:
    @TestUtils.patch_method(PlzApp._main_execute)
    def test_main_configured_called(self, mock_main_execute):
        sys.argv = ["pyplz", "test"]
        main()
        mock_main_execute.assert_called_once()

    @TestUtils.patch_method(PlzApp._main_execute)
    def test_main_main_execute_called(self, mock_main_execute):
        sys.argv = ["pyplz", "test"]
        main()
        mock_main_execute.assert_called_once()

    @pytest.mark.skip("Not implemented")
    @TestUtils.patch_method(PlzApp._main_execute)
    def test_main_parsed_command_executed(self, mock_parse_args, mock_main_execute):
        mocked_command = Mock()
        mock_parse_args.return_value = mocked_command
        sys.argv = ["pyplz", "test"]
        main()
        mock_parse_args.assert_called_once_with(["test"])
        mock_main_execute.assert_called_once_with(mocked_command)
