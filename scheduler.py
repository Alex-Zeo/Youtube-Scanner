import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler

import channel_fetcher
import storage

sys.path.append(str(Path(__file__).resolve().parent / "src"))
from youtube_scanner.logging_config import setup_logging  # noqa: E402

logger = logging.getLogger(__name__)

# List of YouTube channel IDs to scan
CHANNELS: List[str] = []  # Populate with real channel IDs


def run_channel_scan() -> None:
    """Invoke the fetcher for each configured channel."""
    logger.info("Executing scheduled channel scan")
    for channel_id in CHANNELS:
        last_run = storage.get_last_run(channel_id)
        try:
            channel_fetcher.fetch_new_videos(channel_id, last_run)
            storage.update_last_run(channel_id, datetime.utcnow())
            logger.info("Completed fetch for %s", channel_id)
        except Exception as exc:  # pragma: no cover - logging only
            logger.error("Failed to fetch videos for %s: %s", channel_id, exc)


def start() -> BackgroundScheduler:
    """Start the scheduler with a monthly job."""
    scheduler = BackgroundScheduler()
    # Run on the first day of each month at midnight
    scheduler.add_job(run_channel_scan, "cron", day=1, hour=0, minute=0)
    scheduler.start()
    logger.info("Scheduler started with monthly job")
    return scheduler


if __name__ == "__main__":  # pragma: no cover - manual execution only
    setup_logging()
    sched = start()
    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        sched.shutdown()
        logger.info("Scheduler stopped")
