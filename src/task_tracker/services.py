from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path

from task_tracker.manager import manage_json

BASE_DIR = Path(__file__).resolve().parent.parent.parent

STORAGE_PATH = BASE_DIR / "data" / "storage.json"


class TaskStatus(StrEnum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"


@manage_json(STORAGE_PATH, save=True)
def add_task(tasks: dict, description: str) -> dict:
    last_id = max((int(task_id) for task_id in tasks), default=0)
    new_id = str(last_id + 1)

    now_iso = datetime.now(UTC).isoformat()

    tasks[new_id] = {
        "description": description,
        "status": TaskStatus.TODO,
        "created_at": now_iso,
        "updated_at": now_iso,
    }
    return tasks


@manage_json(STORAGE_PATH)
def read_tasks(tasks: dict) -> dict:
    return tasks


@manage_json(STORAGE_PATH)
def filter_tasks_by_status(tasks: dict, status: TaskStatus) -> dict:
    return {
        task_id: task for task_id, task in tasks.items() if task["status"] == status
    }


@manage_json(STORAGE_PATH, save=True)
def update_task(
    tasks: dict,
    task_id: int,
    *,
    description: str | None = None,
    status: TaskStatus | None = None,
) -> dict:
    str_id = str(task_id)
    if str_id not in tasks:
        raise KeyError(f"Task with id {task_id} not found")

    update_data = {}
    if description is not None:
        update_data["description"] = description
    if status is not None:
        update_data["status"] = status

    if not update_data:
        raise ValueError("No fields provided for update")

    update_data["updated_at"] = datetime.now(UTC).isoformat()
    tasks[str_id].update(update_data)

    return tasks


@manage_json(STORAGE_PATH, save=True)
def delete_task(tasks: dict, task_id: int) -> dict:
    str_id = str(task_id)
    if str_id not in tasks:
        raise KeyError(f"Task with id {task_id} not found")

    tasks.pop(str_id)
    return tasks
