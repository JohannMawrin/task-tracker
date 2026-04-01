from typing import Annotated, Any

import typer

from task_tracker import services
from task_tracker.ui import print_task_table

app = typer.Typer(
    rich_markup_mode="rich", context_settings={"help_option_names": ["-h", "--help"]}
)


@app.command()
def add(
    description: Annotated[
        str,
        typer.Argument(help='The description of the task, for example: "Buy milk".'),
    ],
) -> Any:
    tasks = services.add_task(description)
    print_task_table(tasks)


@app.command(name="list")
def task_list(
    status: Annotated[
        services.TaskStatus | None,
        typer.Option("--status", "-s", help="Filter tasks by status."),
    ] = None,
) -> Any:
    if status is None:
        tasks = services.read_tasks()
    else:
        tasks = services.filter_tasks_by_status(status)

    print_task_table(tasks)


@app.command()
def update(
    task_id: Annotated[
        int,
        typer.Argument(help="Task ID.", min=1),
    ],
    description: Annotated[
        str,
        typer.Argument(help='The description of the task, for example: "Buy milk".'),
    ],
) -> Any:
    tasks = services.update_task(task_id, description=description)
    print_task_table(tasks)


@app.command()
def delete(
    task_id: Annotated[
        int,
        typer.Argument(help="Task ID.", min=1),
    ],
) -> Any:
    tasks = services.delete_task(task_id)
    print_task_table(tasks)


@app.command()
def mark(
    task_id: Annotated[
        int,
        typer.Argument(help="Task ID.", min=1),
    ],
    status: Annotated[services.TaskStatus, typer.Argument(help="Task status.")],
) -> Any:
    tasks = services.update_task(task_id, status=status)
    print_task_table(tasks)


def main() -> None:
    app()
