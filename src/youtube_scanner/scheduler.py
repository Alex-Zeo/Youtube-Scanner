"""Schedule monthly scans using cron or APScheduler."""

import logging
from typing import Callable

logger = logging.getLogger(__name__)


def schedule_monthly(job: Callable) -> None:
    """Placeholder for scheduling a monthly scanning job."""
    logger.info("Scheduling monthly job %s", job.__name__)
    # TODO: Implement scheduling logic
