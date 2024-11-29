from __future__ import annotations

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class ConsoleUtils:
    @staticmethod
    def print_box(title: str, rows: list[list[str]], sort: bool = False) -> None:
        if rows is None or len(rows) == 0:
            return

        # assert only 2 columns (only use case for now)
        if any(len(r) != 2 for r in rows):
            raise ValueError("Only supporting 2 columns")

        if sort:
            rows = sorted(rows, key=lambda x: x[0])

        # get the max length between all first items
        max_first_length = max(len(r[0]) for r in rows)
        max_first_length = max(max_first_length, 15)

        max_seoncd_length = max(len(r[1]) for r in rows)
        max_seoncd_length = max(max_seoncd_length, 15)

        table = Table(show_header=False, box=None, show_edge=False)
        table.add_column("1", no_wrap=True, width=max_first_length + 2)
        table.add_column("2", style="white", no_wrap=True, width=max_seoncd_length + 2)

        for r in rows:
            first = f"[bold]{r[0]}[/]" or ""
            second = r[1] or ""
            table.add_row(first, second)

        panel_width = max_first_length + max_seoncd_length + 4

        # Ensure the panel width does not exceed terminal width
        terminal_width = console.size.width

        final_width = min(panel_width, terminal_width)

        panel = Panel(
            table,
            title=title,
            title_align="left",
            border_style="cyan",
            padding=(0, 1),
            box=box.ROUNDED,
            width=final_width,
        )
        console.print(panel)
