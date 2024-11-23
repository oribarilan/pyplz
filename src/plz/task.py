from __future__ import annotations

from typing import Any, Callable
import inspect
from rich.console import Console

console = Console()


class Task:
    def __init__(
        self,
        func: Callable,
        name: str | None = None,
        desc: str | None = None,
        requires: list[tuple[Task, tuple[Any, ...]]] | None = None,
        is_default: bool = False,
        is_builtin: bool = False,
    ) -> None:
        self.func = func
        self.name = name or func.__name__
        desc = desc or ""
        if len(desc) == 0 and func.__doc__ is not None:
            desc = inspect.cleandoc(func.__doc__)
        self.desc = desc
        self.requires = requires or []
        self.is_default = is_default
        self.is_builtin = is_builtin

    def __call__(self) -> Any:
        """
        Call the task function and return the result.
        If the task function has any required functions, they will be called first (recursively).
        """
        required = self.requires or []
        for r in required:
            func, args = r
            ret = func(*args)
            if ret is not None:
                console.log(ret)

        ret = self.func()
        if ret is not None:
            console.log(ret)

    def __str__(self) -> str:
        tags = f"{'[default]' if self.is_default else ''}{'[builtin]' if self.is_builtin else ''}"
        return f"{self.name} {tags}"

    def __repr__(self) -> str:
        return self.__str__()
