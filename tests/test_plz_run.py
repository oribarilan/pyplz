from __future__ import annotations

import subprocess

import pytest

from pyplz import plz


class TestPlzRun:
    def test_run_fails_error_raised(self):
        with pytest.raises(subprocess.CalledProcessError):
            plz.run("ls /non/existent/path", raise_error=True)

    def test_run_fails_error_not_raised(self):
        ec = plz.run("ls /non/existent/path", raise_error=False)
        assert ec != 0

    def test_run_echo_true(self, capfd):
        cmd = "echo hello"

        ec = plz.run(cmd, echo=True)

        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 2
        assert lines[0] == f"Executing: `{cmd}`"
        assert lines[1] == "hello"
        assert ec == 0

    def test_run_echo_false(self, capfd):
        cmd = "echo hello"

        ec = plz.run(cmd, echo=False)

        lines = capfd.readouterr().out.splitlines()
        assert len(lines) == 1
        assert lines[0] == "hello"
        assert ec == 0
