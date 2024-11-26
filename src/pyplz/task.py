from __future__ import annotations

import inspect
from typing import Any, Callable

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table


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

    def __call__(self, *args) -> Any:
        """
        Call the task function and return the result.
        If the task function has any required functions, they will be called first (recursively).
        #"""
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
            return

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
        console = Console()
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

        # Create a table to display the information
        table = Table(show_header=False, box=None)
        if dependencies:
            table.add_row("[bold]Depends on[/bold]", ", ".join(dependencies))
        table.add_row("[bold]Parameters[/bold]", ", ".join(params))
        table.add_row("[bold]Description[/bold]", docstring.strip())

        # Calculate the required width
        max_param_length = max(len(param) for param in params) if params else 0
        max_desc_length = max(len(line) for line in docstring.split("\n"))
        required_width = max(max_param_length, max_desc_length) + 20
        terminal_width = console.size.width
        final_width = min(required_width, terminal_width)

        # Create a panel to enclose the table
        panel = Panel(
            table,
            title=f"{self.name}",
            title_align="left",
            border_style="cyan",
            padding=(0, 1),
            box=box.ROUNDED,
            width=final_width,
        )
        console.print(panel)
