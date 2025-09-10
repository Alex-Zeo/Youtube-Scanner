"""Persist results using JSON or a database."""

import json
import logging
from typing import Any

logger = logging.getLogger(__name__)


def save_results(data: Any, filename: str = "results.json") -> None:
    """Persist data to a JSON file."""
    logger.info("Saving results to %s", filename)
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
