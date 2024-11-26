from __future__ import annotations

import importlib.util
import inspect
import os
import subprocess
import sys
from pathlib import Path
from typing import Callable

from dotenv import dotenv_values, load_dotenv
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from plz.command import Command, Parser
from plz.console_utils import ConsoleUtils
from plz.task import Task
from plz.types import CallableWithArgs

console = Console()


class PlzApp:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = dict()
        self._user_configured = False

    def _configure(self, parser: Parser):
        self._parser = parser

    def configure(self):
        self._user_configured = True
        self._dotenv = self._load_environment_variables()
        # plz loads the CWD to the sys.path to allow plzfile to import freely
        sys.path.append(os.path.join(os.getcwd()))

    def _add_builtin(self, name: str, desc: str, func: Callable) -> None:
        task = Task(func=func, name=name, desc=desc, is_builtin=True, is_default=False)
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

    def _load_environment_variables(self) -> list[list[str]]:
        # Determine the path to the .env file
        env_path = Path(os.getcwd()) / ".env"

        # Load the .env file if it exists
        if env_path.exists():
            # capture the env variables
            load_dotenv(env_path)
            # Load the environment variables into a variable
            env_vars_dict = dotenv_values(env_path)
            env_vars_list = [[k, v] for k, v in env_vars_dict.items() if v is not None]
            return env_vars_list

        return []

    def _try_execute_utility_commands(self, command: Command) -> bool:
        if command.has_task_specified():
            return False

        if command.list:
            self.list_tasks()
            return True

        if command.list_env:
            self._print_env(cmd=command)
            return True

        if command.list_env_all:
            self._print_env(cmd=command, all=True)
            return True

        return False

    def _try_execute_conditional_utility_commands(self, command: Command) -> bool:
        if command.has_task_specified():
            return False

        if command.help:
            self._print_help()
            return True

        return False

    def _get_default_task(self) -> Task | None:
        default_tasks = [t for t in self._tasks.values() if t.is_default]

        if len(default_tasks) > 1:
            self.fail("More than one default task found: " + ", ".join(t.name for t in default_tasks))

        if len(default_tasks) == 0:
            return None
        return default_tasks[0]

    def _try_execute_default_task(self, command: Command) -> bool:
        if command.has_task_specified():
            return False

        if not command.is_default():
            return False

        default_task = self._get_default_task()
        if default_task is None:
            self.list_tasks()
            return True

        return False

    def _try_execute_task(self, command: Command) -> bool:
        if not command.has_task_specified():
            return False

        if command.task not in self._tasks:
            self.fail(f"Task '{command.task}' not found.")
            return False

        task = self._tasks[command.task]

        if command.help:
            task.print_doc()
            return True

        if command.list_env:
            self._print_env(cmd=command)
            return True

        task(*command.args)
        return True

    def _process_env_vars(self, command: Command):
        for k, v in command.env:
            os.environ[k] = v

    def _load_plzfile(self):
        plzfile_path = os.path.join(os.getcwd(), "plzfile.py")
        spec = importlib.util.spec_from_file_location("plzfile", plzfile_path)
        plzfile = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(plzfile)  # type: ignore

    def _main_execute(self, command: Command):
        if not self._user_configured:
            self.configure()

        self._load_plzfile()

        self._process_env_vars(command)

        if self._try_execute_utility_commands(command):
            return

        if self._try_execute_conditional_utility_commands(command):
            return

        if self._try_execute_default_task(command):
            return

        if self._try_execute_task(command):
            return

        self.fail("Execution failed for unknown reason.")

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

            return func

        return decorator

    @staticmethod
    def print_error(msg: str):
        PlzApp.print(msg, "red")

    @staticmethod
    def print_warning(msg: str):
        PlzApp.print(msg, "yellow")

    @staticmethod
    def print_weak(msg: str):
        PlzApp.print(msg, "bright_black")

    @staticmethod
    def print(msg: str, color: str | None = None):
        if color:
            msg = f"[{color}]{msg}[/]"
        console.print(msg)

    @staticmethod
    def fail(msg: str | None = None):
        if msg is not None:
            PlzApp.print_error(msg)
        sys.exit(1)

    def _print_help(self):
        """Print the general help message."""
        self._parser.parser.print_help()
        self.print(r"Usage: [orange1]plz \[task] \[args][/]")
        self.print("\nAvailable flags:")
        self.print("  -h, --help    Show help for a specific task (or for plz if no task is provided)")
        self.print("  -l, --list    List all available tasks")
        self.print("\nAvailable tasks:")
        self.list_tasks()

    def _print_env(self, cmd: Command, all: bool = False):
        """
        prints the environment variable
        """
        ConsoleUtils.print_box(title=".env", rows=self._dotenv, sort=True)
        ConsoleUtils.print_box(title="in-line", rows=cmd.env, sort=True)
        if all:
            env_vars = os.environ
            rows = [[key, value] for key, value in env_vars.items()]
            rows = [row for row in rows if row not in self._dotenv]
            ConsoleUtils.print_box(title="All (rest)", rows=rows, sort=True)

    def _run_cli_command(
        self, cli_command: str, print: bool = True, env: dict[str, str] | None = None
    ) -> tuple[str, int]:
        try:
            # Open a subprocess
            process = subprocess.Popen(
                cli_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env, shell=True
            )
            output = ""
            # Stream the output in real-time
            if process.stdout is None:
                return "", 1

            for line in process.stdout:
                output += line
                if print:
                    self.print(line.rstrip())

            # Wait for the process to finish and get the return code
            return_code = process.wait()
            if return_code != 0:
                self.print_error(f"\nCommand failed with exit code {return_code}")

        except Exception as e:
            return_code = 1
            output = f"Error running command: {e}"
            self.print(output)

        return output, return_code

    def run(
        self,
        command: str,
        env: dict[str, str] | None = None,
        timeout_secs: int | None = None,
        dry_run: bool = False,
        echo: bool = True,
        print: bool = True,
    ) -> tuple[str, int]:
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
            self.print_weak(f"Executing: `{command}`")

        if dry_run:
            self.print_warning(f"Dry run: {command}")
            return ("", 0)

        # Merge provided env with the current environment variables
        env = {**os.environ, **(env or {})}

        try:
            output_str, exit_code = self._run_cli_command(command, env=env)
            return output_str, exit_code
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command '{command}' failed with error: {e}")
        except subprocess.TimeoutExpired as e:
            self.print_error(f"Command '{command}' timed out after {timeout_secs} seconds, {e}")

        return ("", 1)


plz = PlzApp()
