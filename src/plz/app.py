import typer
from typing import Callable, Dict
import importlib.util
import os


class Plz:
    def __init__(self):
        self.app = typer.Typer()
        self.tasks: Dict[str, Callable] = {}
        self.default_task: Optional[Callable[[], None]] = None
        self.app.command()(self.list)
        self.app.callback()(self.list)

    def task(self, name: str = None):
        """A decorator to register tasks."""

        def wrapper(func: Callable):
            task_name = name or func.__name__
            self.tasks[task_name] = func
            self.app.command(task_name)(func)  # Register the task as a Typer command
            return func

        return wrapper

    def default(self):
        """A decorator to register the default task."""

        def wrapper(func: Callable):
            self.default_task = func
            return func

        return wrapper

    def run(self):
        # Load and execute plz.py if it exists
        if os.path.exists("plz.py"):
            spec = importlib.util.spec_from_file_location("plz", "plz.py")
            plz_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plz_module)
        else:
            typer.echo("No plz.py found in the root directory. Listing available tasks:")
            # self.list_tasks()
            return

        self.app()

    def list(self):
        """List all available tasks."""
        if not self.tasks:
            self.log("No tasks have been registered.")
            return
        self.log("Available tasks:")
        for task_name, task_func in self.tasks.items():
            doc = task_func.__doc__ or "No description."
            self.log(f"\t{task_name}: {doc.strip()}")

    def log(self, msg: str):
        """Log a message. Use this instead of print."""
        typer.echo(msg)


def main():
    plz.run()


plz = Plz()
