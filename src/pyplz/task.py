from __future__ import annotations

import inspect
import os
import sys
from typing import Any, Callable

from rich.console import Console

from pyplz.console_utils import ConsoleUtils


console = Console()


class Task:
    def __init__(
        self,
        func: Callable,
        name: str | None = None,
        desc: str | None = None,
        requires: list[tuple[Task, tuple]] | None = None,  # List of tuples of tasks and their arguments
        is_default: bool = False,
        is_builtin: bool = False,
        task_env_vars: dict[str, Any] | None = None,
    ) -> None:
        self.func = func
        self.name = name or func.__name__
        desc = desc or ""
        if len(desc) == 0 and func.__doc__ is not None:
            desc = inspect.cleandoc(func.__doc__)
        self.desc = desc
        self.is_default = is_default
        self.is_builtin = is_builtin

        # normalize requires
        if requires is None:
            requires = []
        self.requires = requires

        # normalize task-scope environment variables
        if task_env_vars is None:
            task_env_vars = {}
        self.task_env_vars = task_env_vars

    def __call__(self, *args) -> Any:
        """
        Call the task function and return the result.
        If the task function has any required functions, they will be called first (recursively).
        #"""
        # load task-level environment variables
        for key, value in self.task_env_vars.items():
            os.environ[key] = value

        # Invoke required tasks first
        for r_task, r_args in self.requires:
            r_task(*r_args)

        # Get the required positional arguments
        sig = inspect.signature(self.func)
        params = [
            param
            for param in sig.parameters.values()
            if param.default == inspect.Parameter.empty
            and param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        ]

        # Check for missing arguments
        if len(args) < len(params):
            args_num = len(args)
            missing_params = params[args_num:]
            missing = ", ".join(p.name for p in missing_params)
            console.print(f"[red]Missing arguments for task '{self.name}': {missing}[/]")
            sys.exit(1)

        ret = self.func(*args)
        if ret is not None:
            console.print(ret)

    def __str__(self) -> str:
        tags = f"{'[default]' if self.is_default else ''}{'[builtin]' if self.is_builtin else ''}"
        return f"{self.name} {tags}"

    def __repr__(self) -> str:
        return self.__str__()

    def print_doc(self):
        """Print the documentation of the task, including parameters."""
        sig = inspect.signature(self.func)

        # Build parameters list with types, default values, and optionality
        params = []
        for param in sig.parameters.values():
            param_type = f": {param.annotation.__name__}" if param.annotation != inspect.Parameter.empty else ""
            if param.default is inspect.Parameter.empty:
                params.append(f"[cyan]{param.name}{param_type}[/cyan]")
            else:
                default_value = f" = {param.default!r}"
                params.append(f"[cyan]{param.name}{param_type}{default_value}[/cyan] [grey70](optional)[/grey70]")

        # Build dependencies list
        dependencies = [r_task.name for r_task, r_args in self.requires]

        # Get the docstring
        docstring = self.desc or "No description provided."

        rows = []
        if dependencies:
            dependencies_line = ["Requires", ", ".join(dependencies)]
            rows.append(dependencies_line)
        parameters_line = ["Parameters", ", ".join(params)]
        rows.append(parameters_line)
        desc_line = ["Description", docstring.strip()]
        rows.append(desc_line)

        ConsoleUtils.print_box(self.name, rows, sort=False)

        env_vars_values = [[k, v] for k, v in self.task_env_vars.items()]
        ConsoleUtils.print_box("Task-defined Environment", env_vars_values)
