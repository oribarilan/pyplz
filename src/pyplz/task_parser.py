import argparse
import inspect
from typing import Union, get_args, get_origin

from pyplz.command import Command
from pyplz.exceptions import ForwardRefrenceNotSupported
from pyplz.task import Task


class TaskParser:
    def __init__(self):
        self._parser = argparse.ArgumentParser(add_help=False)

    @staticmethod
    def _is_nullable(param_type) -> bool:
        origin = get_origin(param_type)
        if origin is Union:
            return type(None) in get_args(param_type)
        return False

    def _add_task_arguments(self, task: Task):
        """Dynamically add arguments to the task parser based on the task's signature."""
        sig = inspect.signature(task.func)
        self._parser.description = task.desc
        g_system = self._parser.add_argument_group(title="system options")
        g_required = self._parser.add_argument_group(title="required arguments")
        g_optional = self._parser.add_argument_group(title="optional arguments")
        g_system.add_argument(
            "-h",
            "--help",
            action="help",
            default=argparse.SUPPRESS,
            help="Show this help message and exit.",
        )
        for name, param in sig.parameters.items():
            arg_name = f"--{name.replace('_', '-')}"
            param_type = param.annotation
            if type(param_type) is str:
                raise ForwardRefrenceNotSupported()
            is_nullable = self._is_nullable(param_type)
            has_default = param.default != inspect.Parameter.empty
            # we allow not setting an arg if it's optional or has a default value
            is_required = not is_nullable and not has_default

            kwargs = {}
            brackets_info = []
            brackets_info.append(param_type.__name__)

            # annotation is the type hint, can either be a type or a string
            # (in case of forward references using __future__)
            if param.annotation is bool:
                help = f"Set {name} to true"
                # bool is a special case, as it's always optional
                is_required = False
                if has_default and param.default is True:
                    brackets_info.append("default: true")
                    default = True
                    action = "store_false"
                else:
                    brackets_info.append("default: false")
                    default = False
                    action = "store_true"
                kwargs["default"] = default
            else:
                help = f"Set {name} to the provided value"
                action = "store"
                if has_default:
                    default = param.default
                    kwargs["default"] = default
                    brackets_info.append(f"default: {default}")
                kwargs["type"] = param_type

            help += f" ({', '.join(brackets_info)})"

            group = g_required if is_required else g_optional

            group.add_argument(
                arg_name,
                action=action,
                help=help,
                required=is_required,
                **kwargs,
            )

    def parse(self, task: Task, args: list[str]):
        self._add_task_arguments(task)
        parsed_args = self._parser.parse_args(args)
        kwargs = {k.replace("-", "_"): v for k, v in vars(parsed_args).items()}
        return Command(
            task=task,
            task_kwargs=kwargs,
        )
