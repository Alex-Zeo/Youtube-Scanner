"""Schedule monthly channel scans using APScheduler."""

from datetime import datetime
import logging
from typing import List, Optional

from apscheduler.schedulers.background import BackgroundScheduler

from . import channel_fetcher, storage

logger = logging.getLogger(__name__)

# List of YouTube channel IDs to scan
CHANNELS: List[str] = []  # Populate with real channel IDs
# API key for YouTube Data API
API_KEY: str = ""  # Populate with a valid API key

# Hold reference to running scheduler for clean shutdown
_scheduler: Optional[BackgroundScheduler] = None


def run_channel_scan() -> None:
    """Invoke the fetcher for each configured channel."""
    logger.info("Executing scheduled channel scan")
    for channel_id in CHANNELS:
        last_run = storage.get_last_run(channel_id)
        try:
            channel_fetcher.fetch_channel_videos(API_KEY, channel_id)
            storage.update_last_run(channel_id, datetime.utcnow())
            logger.info("Completed fetch for %s", channel_id)
        except Exception as exc:  # pragma: no cover - logging only
            logger.error("Failed to fetch videos for %s: %s", channel_id, exc)


def start() -> BackgroundScheduler:
    """Start the scheduler with a monthly job.

    Returns
    -------
    BackgroundScheduler
        The running scheduler instance.
    """
    global _scheduler
    scheduler = BackgroundScheduler()
    # Run on the first day of each month at midnight
    scheduler.add_job(run_channel_scan, "cron", day=1, hour=0, minute=0)
    scheduler.start()
    _scheduler = scheduler
    logger.info("Scheduler started with monthly job")
    return scheduler


def stop(scheduler: Optional[BackgroundScheduler] = None) -> None:
    """Shutdown the scheduler if running."""
    sched = scheduler or _scheduler
    if sched and sched.running:
        sched.shutdown()
        logger.info("Scheduler stopped")
