from __future__ import annotations

from dataclasses import dataclass
from typing import List

from pyplz.task import Task


@dataclass
class Command:
    task: Task | None = None
    task_kwargs: dict[str, str] | None = None
    list: bool = False
    help: bool = False
    show_env: bool = False
    show_env_all: bool = False
    _env: List[str] | None = None
    _args: List[str] | None = None

    def has_task_specified(self) -> bool:
        return self.task is not None

    def is_default(self) -> bool:
        has_any_utility_flag = self.list or self.help or self.show_env or self.show_env_all
        return not self.has_task_specified() and not has_any_utility_flag

    @property
    def env(self) -> List[List[str]]:
        return [env.split("=") for env in self._env] if self._env else []

    @property
    def args(self) -> List[str]:
        return self._args or []
