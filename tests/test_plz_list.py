from __future__ import annotations

from pyplz import plz
from pyplz.command import Command


class TestPlzList:
    def test_list_without_tasks(self, capfd):
        cmd = Command(list=True)

        plz._main_execute(cmd)

        assert len(plz._tasks) == 0
        out = capfd.readouterr().out
        assert "No tasks have been registered" in out
