"""Schedule monthly scans using cron or APScheduler."""

from typing import Callable
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def schedule_monthly(job: Callable) -> None:
    """Placeholder for scheduling a monthly scanning job."""
    logger.info("Scheduling monthly job %s", job.__name__)
    # TODO: Implement scheduling logic
