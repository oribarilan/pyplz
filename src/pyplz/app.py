from __future__ import annotations

import inspect
import subprocess
import sys
from typing import Callable

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from pyplz.task import Task
from pyplz.types import CallableWithArgs

console = Console()


class Plz:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = dict()

    def _add_builtin(self, name: str, desc: str, func: Callable, default: bool = False) -> None:
        task = Task(func=func, name=name, desc=desc, is_builtin=True, is_default=default)
        self._tasks[task.name] = task

    def list_tasks(self):
        """List all available tasks."""
        if all(t.is_builtin for t in self._tasks.values()):
            self.print_error("No tasks have been registered. plz expects at least one `@plz.task` in your plzfile.py")
            return

        max_command_length = max(len(t.name) + 5 for t in self._tasks.values())
        max_command_length = min(max_command_length, 25)

        max_desc_length = max(len(t.desc) * 2 for t in self._tasks.values() if t.desc is not None)
        max_desc_length = min(max_desc_length, 50)

        table = Table(show_header=False, box=None, show_edge=False)
        table.add_column("Tasks", style="orange1", no_wrap=True, width=max_command_length + 2)
        table.add_column("Description", style="white", no_wrap=True, width=max_desc_length + 2)

        for t in self._tasks.values():
            desc = t.desc or ""
            name = t.name
            if t.is_default:
                name = f"[bold]{name}[/bold]"
                desc = f"[bold]{desc}\t(default)[/bold]"
            table.add_row(f"{name}", desc)

        panel_width = max_command_length + max_desc_length + 4

        # Ensure the panel width does not exceed terminal width
        terminal_width = console.size.width

        final_width = min(panel_width, terminal_width)

        panel = Panel(
            table,
            title="Tasks",
            title_align="left",
            border_style="dark_orange3",
            padding=(0, 1),
            box=box.ROUNDED,
            width=final_width,
        )
        console.print(panel)

    def _run_task(self, task_name: str | None, *args):
        arg_lst = list(args)

        # handle list
        if task_name is not None and (task_name == "-l" or task_name == "--list"):
            self.list_tasks()
            return

        # handle help
        if task_name is not None and (task_name == "-h" or task_name == "--help"):
            self._print_help()
            return

        # default
        if task_name is None:
            default_tasks = [t for t in self._tasks.values() if t.is_default]

            if len(default_tasks) > 1:
                self.print_error("More than one default task found: " + ", ".join(t.name for t in default_tasks))
                sys.exit(1)

            if len(default_tasks) == 0:
                # default behavior is to list tasks
                self.list_tasks()
                return

            default_task = default_tasks[0]
            default_task()
            return

        # specified
        if task_name in self._tasks:
            task = self._tasks[task_name]

            # handle help
            if "-h" in arg_lst or "--help" in arg_lst:
                task.print_doc()
                return

            task(*args)
            return

        # not found
        self.print_error(f"Task '{task_name}' not found.")

    def task(
        self,
        name: str | None = None,
        desc: str | None = None,
        default: bool = False,
        requires: Callable | list[Callable | CallableWithArgs] | None = None,
    ) -> Callable:
        def decorator(func) -> Callable:
            t_name = name
            if name is None:
                t_name = func.__name__

            t_desc = desc
            if desc is None:
                t_desc = inspect.cleandoc(func.__doc__) if func.__doc__ else ""

            # Nomralize requires to list of tuples
            _required = requires
            required_funcs: list[CallableWithArgs]
            if _required is None:
                required_funcs = []
            elif isinstance(_required, list):
                # Normalize callable with args to tuple as well
                required_funcs = [r if isinstance(r, tuple) else (r, ()) for r in _required]
            else:
                required_funcs = [(_required, ())]
            required_tasks = [(self._tasks[r.__name__], args) for r, args in required_funcs]

            self._tasks[func.__name__] = Task(
                func=func, name=t_name, desc=t_desc, is_default=default, requires=required_tasks
            )
            if default:
                # set all builtins to not be default
                for t in (t for t in self._tasks.values() if t.is_builtin):
                    t.is_default = False

            return func

        return decorator

    def print_error(self, msg: str):
        self.print(msg, "red")

    def print_warning(self, msg: str):
        self.print(msg, "yellow")

    def print_weak(self, msg: str):
        self.print(msg, "bright_black")

    def print(self, msg: str, color: str | None = None):
        if color:
            msg = f"[{color}]{msg}[/]"
        console.print(msg)

    def _print_help(self):
        """Print the general help message."""
        console.print(r"Usage: [orange1]plz \[task] \[args][/]")
        console.print("\nAvailable flags:")
        console.print("  -h, --help    Show help for a specific task (or for plz if no task is provided)")
        console.print("  -l, --list    List all available tasks")
        console.print("\nAvailable tasks:")
        self.list_tasks()

    def run(
        self,
        command: str,
        env: dict[str, str] | None = None,
        timeout_secs: int | None = None,
        dry_run: bool = False,
        echo: bool = True,
        print: bool = True,
    ) -> str | None:
        """
        Executes a shell command with optional environment variables, timeout, and dry run mode.
        Args:
            command (str): The shell command to execute.
            env (dict[str, str], optional): A dictionary of environment variables to set for the command.
                Defaults to None.
            timeout_secs (int, optional): The maximum number of seconds to allow the command to run. Defaults to None.
            dry_run (bool): If True, the command will not be executed, and a dry run message will be printed.
                Defaults to False.
            echo (bool): If True, the command will be printed before execution. Defaults to True.
            print (bool): If True, the standard output of the command will be printed. Defaults to True.
        Returns:
            The standard output of the command, or None if the command failed.
        Raises:
            subprocess.CalledProcessError: If the command returns a non-zero exit status.
            subprocess.TimeoutExpired: If the command times out.
        """
        if echo:
            self.print_weak(f"Running command: `{command}`")

        if dry_run:
            self.print_warning(f"Dry run: {command}")
            return None

        try:
            result = subprocess.run(
                command, shell=True, check=True, text=True, capture_output=True, env=env, timeout=timeout_secs
            )
            if print and result.stdout:
                self.print(result.stdout)
            if result.stderr:
                self.print_error(result.stderr)
                return None
            return result.stdout
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command '{command}' failed with error: {e}")
        except subprocess.TimeoutExpired as e:
            self.print_error(f"Command '{command}' timed out after {timeout_secs} seconds, {e}")

        return None


plz = Plz()
