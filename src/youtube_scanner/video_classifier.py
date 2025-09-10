"""Determine Shorts vs. long-form videos by duration."""

import logging
from typing import Dict
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def classify_video(duration_seconds: int) -> str:
    """Classify a video based on its duration."""
    classification = "short" if duration_seconds <= 60 else "long"
    logger.info("Classified duration %s as %s", duration_seconds, classification)
    return classification


def is_short(video_info: Dict[str, int]) -> bool:
    """Return ``True`` if the video should be classified as a YouTube Short."""
    duration = video_info.get("duration", 0)
    logger.debug("Classifying video with duration %s", duration)
    return classify_video(duration) == "short"
