import logging
from typing import Dict

logger = logging.getLogger(__name__)


def classify_duration(duration: int) -> str:
    """Return ``"short"`` or ``"long"`` based on the video's duration.

    According to the project README, videos of 60 seconds or less are
    considered YouTube Shorts, while anything longer is treated as a
    long-form video.
    """
    logger.debug("Classifying video with duration %s", duration)
    return "short" if duration <= 60 else "long"


def is_short(video_info: Dict[str, int]) -> bool:
    """Return ``True`` if the video should be classified as a YouTube Short.

    This helper is kept for backward compatibility. New code should
    prefer :func:`classify_duration`.
    """
    duration = video_info.get("duration", 0)
    return classify_duration(duration) == "short"
