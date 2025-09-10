"""Determine Shorts vs. long-form videos by duration."""

import logging

logger = logging.getLogger(__name__)


def classify_video(duration_seconds: int) -> str:
    """Classify a video based on its duration."""
    classification = "short" if duration_seconds <= 60 else "long"
    logger.info(
        "Classified duration %s as %s",
        duration_seconds,
        classification,
    )
    return classification
