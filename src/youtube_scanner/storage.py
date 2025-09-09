"""Persist results using JSON or a database."""

import json
from typing import Any
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def save_results(data: Any, filename: str = "results.json") -> None:
    """Persist data to a JSON file."""
    logger.info("Saving results to %s", filename)
    with open(filename, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
