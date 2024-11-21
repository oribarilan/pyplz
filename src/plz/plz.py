from typing import Callable, Dict

import typer


class Plz(typer.Typer):
    def __init__(self):
        super().__init__()  # Initialize Typer
        self.tasks: Dict[str, Callable] = {}

    def task(self, name: str):
        """A decorator to register tasks."""
        def wrapper(func: Callable):
            self.tasks[name] = func
            self.command(name)(func)  # Register the task as a Typer command
            return func
        return wrapper

    def list_tasks(self):
        """List all available tasks."""
        for task_name, task_func in self.tasks.items():
            print(f"{task_name}: {task_func.__doc__}")
