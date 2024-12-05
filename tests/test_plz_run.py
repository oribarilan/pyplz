from __future__ import annotations

import subprocess

import pytest

from pyplz import plz
from tests.conftest import TestUtils


class TestPlzRun:
    def test_run_returns_output_and_code(self):
        output = plz.run("echo hello")
        assert output == "hello"

    def test_run_returns_multiline_output_and_code(self):
        output = plz.run("echo 'hello\nworld\nechoed'")
        assert output == "hello\nworld\nechoed"

    def test_run_fails_returns_stderr(self):
        output = plz.run("ls /non/existent/path", raise_error=False)
        assert "No such file or directory" in output

    def test_run_returns_error_output_and_code_with_raise_on_error(self):
        with pytest.raises(subprocess.CalledProcessError):
            plz.run("ls /non/existent/path", raise_error=True)

    def test_run_timeout(self):
        with pytest.raises(subprocess.TimeoutExpired):
            plz.run("sleep 5", timeout_secs=1)

    def test_run_echo_true(self, capfd):
        cmd = "echo hello"
        plz.run(cmd, echo=True)
        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 2
        assert lines[0] == f"Executing: `{cmd}`"
        assert lines[1] == "hello"

    def test_run_echo_false(self, capfd):
        cmd = "echo hello"
        plz.run(cmd, echo=False)
        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 1
        assert lines[0] == "hello"

    @TestUtils.patch_method(plz._run_cli_command)
    def test_run_dry_run(self, run_cli_command_mock, capfd):
        cmd = "echo hello"
        plz.run(cmd, dry_run=True)
        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 1
        assert lines[0] == "Dry run: `echo hello`"
        run_cli_command_mock.assert_not_called()

    def test_run_silent(self, capfd):
        cmd = "echo hello"
        plz.run(cmd, silent=True)
        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 1
        assert lines[0] == "Executing: `echo hello`"

    def test_run_silent_without_echo(self, capfd):
        cmd = "echo hello"
        plz.run(cmd, silent=True, echo=False)
        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 0
