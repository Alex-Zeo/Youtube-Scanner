import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# File used to persist last run timestamps per channel
_STORAGE_FILE = Path("last_run.json")


def _load_data() -> Dict[str, datetime]:
    """Load persisted timestamps from disk."""
    if _STORAGE_FILE.exists():
        try:
            with _STORAGE_FILE.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            return {key: datetime.fromisoformat(value) for key, value in data.items()}
        except Exception as exc:  # pragma: no cover - logging only
            logging.error("Failed to load last run timestamps: %s", exc)
    return {}


def _save_data(data: Dict[str, datetime]) -> None:
    """Persist timestamps to disk."""
    serialised = {key: value.isoformat() for key, value in data.items()}
    try:
        with _STORAGE_FILE.open("w", encoding="utf-8") as fh:
            json.dump(serialised, fh)
        logging.info("Persisted last run timestamps")
    except Exception as exc:  # pragma: no cover - logging only
        logging.error("Failed to persist last run timestamps: %s", exc)


def get_last_run(channel_id: str) -> Optional[datetime]:
    """Return the last run timestamp for the provided channel."""
    data = _load_data()
    return data.get(channel_id)


def update_last_run(channel_id: str, timestamp: datetime) -> None:
    """Update the last run timestamp for the provided channel."""
    data = _load_data()
    data[channel_id] = timestamp
    _save_data(data)
