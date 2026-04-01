from datetime import datetime
from types import MappingProxyType

from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text

from task_tracker.services import TaskStatus

STYLES = MappingProxyType({
    "table_header": Style(color="bright_black", bold=True),
    "table_border": Style(color="bright_black"),
    "secondary_color": Style(color="bright_black"),
    "statuses": {
        TaskStatus.TODO: Style(color="black", bgcolor="red", bold=True),
        TaskStatus.IN_PROGRESS: Style(color="black", bgcolor="yellow", bold=True),
        TaskStatus.DONE: Style(color="black", bgcolor="green", bold=True),
    },
})


def _make_status(name: str) -> Text:
    style = STYLES["statuses"].get(name)
    return Text(name, style=style, justify="center")


def _make_last_update(date: str) -> str:
    return datetime.fromisoformat(date).strftime("%d.%m.%Y")


console = Console()


def print_task_table(tasks: dict) -> Table:
    table = Table(
        box=box.SIMPLE,
        expand=True,
        header_style=STYLES.get("table_header"),
        border_style=STYLES.get("table_border"),
    )
    table.add_column("ID", style=STYLES.get("secondary_color"))
    table.add_column("DESCRIPTION", ratio=1)
    table.add_column("STATUS")
    table.add_column("LAST UPDATE", style=STYLES.get("secondary_color"))

    for task_id, task in tasks.items():
        status = _make_status(task["status"])
        last_update = _make_last_update(task["updated_at"])

        table.add_row(
            task_id,
            task["description"],
            status,
            last_update,
        )

    console.print(table)
