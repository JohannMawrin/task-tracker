import json
import logging
from functools import wraps
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _load_json(file_path: Path) -> Any:
    if not file_path.exists():
        return {}

    raw_text = file_path.read_text(encoding="utf-8")

    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        logger.exception(f"Failed to decode JSON from: {file_path}")
        return {}


def _save_json(payload: Any, file_path: Path) -> None:
    file_path.mkdir(parents=True, exist_ok=True)

    serialized = json.dumps(payload, ensure_ascii=False, indent=2)
    file_path.write_text(serialized, encoding="utf-8")


def _manage_json(file_path: Path, *, save: bool = False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            payload = _load_json(file_path)

            updated = func(payload, *args, **kwargs)

            if save:
                _save_json(updated, file_path)

            return updated

        return wrapper

    return decorator
