import logging
from typing import Dict

logger = logging.getLogger(__name__)


def is_short(video_info: Dict[str, int]) -> bool:
    """Return True if the video should be classified as a YouTube Short."""
    duration = video_info.get("duration", 0)
    logger.debug("Classifying video with duration %s", duration)
    return duration <= 60
