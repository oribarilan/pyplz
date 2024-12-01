from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List


@dataclass
class Command:
    task: str | None = None
    list: bool = False
    help: bool = False
    list_env: bool = False
    list_env_all: bool = False
    _env: List[str] | None = None
    _args: List[str] | None = None

    def has_task_specified(self) -> bool:
        return self.task is not None

    def is_default(self) -> bool:
        has_any_utility_flag = self.list or self.help or self.list_env or self.list_env_all
        return not self.has_task_specified() and not has_any_utility_flag

    @property
    def env(self) -> List[List[str]]:
        return [env.split("=") for env in self._env] if self._env else []

    @property
    def args(self) -> List[str]:
        return self._args or []


class Parser:
    def __init__(
        self,
    ):
        self.parser = argparse.ArgumentParser(description="plz - A python-first task runner.", add_help=False)
        self.parser.add_argument("task", nargs="?", help="The command to run")
        self.parser.add_argument("-l", "--list", action="store_true", help="List all available tasks")
        self.parser.add_argument(
            "-h",
            "--help",
            action="store_true",
            help="Show help for a specific task (or for plz if no task is provided)",
        )
        self.parser.add_argument(
            "--list-env",
            action="store_true",
            help="List dedicated environment variables for the task (or for plz if no task is provided)",
        )
        self.parser.add_argument("--list-env-all", action="store_true", help="List all environment variables")
        self.parser.add_argument(
            "-e",
            "--env",
            action="append",
            type=str,
            help="Set an environment variable (can be used multiple times). Example: -e KEY=VALUE",
        )
        self.parser.add_argument("args", nargs=argparse.REMAINDER, help="Additional arguments for the task")

    def _split_env_vars_from_args(self, args: List[str]) -> tuple[List[str], List[str]]:
        env_vars = []
        arguments = []
        i = 0
        while i < len(args):
            if (args[i] == "-e" or args[i] == "--env") and i + 1 < len(args):
                env_vars.append(args[i + 1])
                i += 2
            else:
                arguments.append(args[i])
                i += 1
        return env_vars, arguments

    def parse_args(self, argv: list[str]) -> Command:
        args = self.parser.parse_args(argv)

        generic_task_flags = ["-h", "--help", "--list-env"]
        clean_args = [arg for arg in args.args if arg not in generic_task_flags]

        task_env_vars, arguments = self._split_env_vars_from_args(clean_args)

        # join both env vars list
        args.env = args.env or []
        args.env.extend(task_env_vars)

        return Command(
            task=args.task,
            list=args.list,
            help=args.help,
            list_env=args.list_env,
            list_env_all=args.list_env_all,
            _env=args.env,
            _args=arguments,
        )
