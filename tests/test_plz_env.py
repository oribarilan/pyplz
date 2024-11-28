from __future__ import annotations

import os
import tempfile
from pathlib import Path

from pyplz import plz
from pyplz.command import Command
from tests.test_utils import TestUtils


class TestPlzEnv:
    @TestUtils.patch_method(plz._get_dotenv_path)
    def test_load_environment_variables(self, get_dotenv_path_mock):
        dotenv_content = "KEY1=value1\nKEY2=value2\nKEY3=value3"
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(dotenv_content.encode())
            tmp.seek(0)
            get_dotenv_path_mock.return_value = Path(tmp.name)
            plz._load_environment_variables()
            assert os.getenv("KEY1"), "value1"
            assert os.getenv("KEY2"), "value2"
            assert os.getenv("KEY3"), "value3"

    @TestUtils.patch_method(plz._load_environment_variables)
    def test_environment_variables_loaded(self, load_environment_variables_mock):
        cmd = Command()
        plz._main_execute(cmd)
        load_environment_variables_mock.assert_called_once()

    @TestUtils.patch_method(plz._process_env_vars)
    def test_inline_env_vars_loading_called(self, process_env_vars_mock):
        cmd = Command()
        plz._main_execute(cmd)
        process_env_vars_mock.assert_called_once()

    def test_inline_env_vars_loading_loaded(self):
        cmd = Command(None, _env=["KEY1=value1", "KEY2=value2", "KEY3=value3"])
        plz._main_execute(cmd)
        assert os.getenv("KEY1"), "value1"
        assert os.getenv("KEY2"), "value2"
        assert os.getenv("KEY3"), "value3"
