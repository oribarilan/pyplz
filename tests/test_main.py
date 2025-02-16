import sys

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
