"""Small JSON persistence helpers for conversation history."""

import json
from pathlib import Path
from typing import Any


def load_memory(filename: str = "memory.json") -> list[dict[str, str]]:
    """Load conversation messages, returning an empty list if none exist."""
    path = Path(filename)
    if not path.exists():
        return []

    try:
        data: Any = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read {path}; starting with empty memory.")
        return []

    if not isinstance(data, list):
        print(f"Warning: {path} does not contain a JSON list; starting empty.")
        return []

    # Keep only valid user/assistant messages to avoid malformed API input.
    messages = []
    for item in data:
        if (
            isinstance(item, dict)
            and item.get("role") in {"user", "assistant"}
            and isinstance(item.get("content"), str)
        ):
            messages.append({"role": item["role"], "content": item["content"]})
    return messages


def save_memory(messages: list[dict[str, str]], filename: str = "memory.json") -> None:
    """Save messages as readable UTF-8 JSON."""
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(messages, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def clear_memory(filename: str = "memory.json") -> None:
    """Replace saved history with an empty JSON list."""
    save_memory([], filename)
