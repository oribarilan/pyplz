from __future__ import annotations

from ast import Call
import importlib.util
import os
from typing import Any, Callable, Tuple

import typer
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import inspect


_app = typer.Typer(add_completion=False)
console = Console()


class Plz:
    def __init__(self) -> None:
        _app.command(name="list", help="List all available tasks")(self.list)

        self._default_task: Callable[[], None] = self.list

        @_app.callback(invoke_without_command=True)
        def callback(ctx: typer.Context):
            # call the default task if no subcommand is provided
            if ctx.invoked_subcommand is None:
                self._default_task()

    def task(
        self,
        name: str | None = None,
        default: bool = False,
        requires: list[Callable | Tuple[Callable, Tuple[Any, ...]]] | None = None,
    ) -> Callable:
        """A decorator to register tasks."""

        require_func_with_args_collection: list[Callable[[], None]] = []
        if requires:
            if not isinstance(requires, list):
                requires = [requires]

            for r in requires:
                if not isinstance(r, tuple):
                    require_func_with_args = r
                else:
                    func_to_call, arguments = r

                    def require_func_with_args():
                        func_to_call(*arguments)

                require_func_with_args_collection.append(require_func_with_args)

        def wrapper(func: Callable):
            task_name = name or func.__name__
            task_doc = inspect.cleandoc(func.__doc__) if func.__doc__ else ""

            def func_with_requires():
                if requires:
                    for r in require_func_with_args_collection:
                        r()
                return func()

            _app.command(name=task_name, help=task_doc)(func_with_requires)  # Register the task as a Typer command
            if default:
                self._default_task = func
            return func

        return wrapper

    def run(self):
        # Load and execute plz.py if it exists
        if os.path.exists("plzfile.py"):
            spec = importlib.util.spec_from_file_location("plz", "plzfile.py")
            plz_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plz_module)
        else:
            typer.echo(
                "No plzfile (plzfile.py) found in the root directory.\n"
                "Please refer to the documentation for more information."
            )
            return
        _app()

    def list(self):
        """List all available tasks."""
        builtins = ["list"]
        if len(_app.registered_commands) == len(builtins):
            console.print(
                "[red]No tasks have been registered. plz expects at least one `@plz.task` in your plzfile.py[/red]"
            )
            return

        max_command_length = max(
            len(command.name) + 5 for command in _app.registered_commands if command.name is not None
        )
        max_command_length = min(max_command_length, 25)

        max_desc_length = max(len(command.help) * 2 for command in _app.registered_commands if command.help is not None)
        max_desc_length = min(max_desc_length, 50)

        table = Table(show_header=False, box=None, show_edge=False)
        table.add_column("Commands", style="cyan", no_wrap=True, width=max_command_length + 2)
        table.add_column("Description", style="white", no_wrap=True, width=max_desc_length + 2)

        for command in _app.registered_commands:
            if command.name is None:
                continue

            description = command.help or ""
            name = command.name
            if command.callback is self._default_task:
                name = f"[bold]{name}[/bold]"
                description = f"[bold]{description}\t(default)[/bold]"
            table.add_row(f"{name}", description)

        panel_width = max_command_length + max_desc_length + 4

        # Ensure the panel width does not exceed terminal width
        terminal_width = console.size.width

        final_width = min(panel_width, terminal_width)

        panel = Panel(
            table,
            title="Commands",
            title_align="left",
            border_style="cyan",
            padding=(0, 1),
            box=box.ROUNDED,
            width=final_width,
        )
        console.print(panel)

    def log(self, msg: str):
        """Log a message. Use this instead of print."""
        typer.echo(msg)


def main():
    plz.run()


plz = Plz()
