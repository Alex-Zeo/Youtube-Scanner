import logging
from typing import Dict, Iterable, Optional

logger = logging.getLogger(__name__)


def map_short_to_long(short: Dict[str, str], videos: Iterable[Dict[str, str]]) -> Optional[Dict[str, str]]:
    """Map a short video to a matching long-form video by title."""
    logger.info("Mapping short %s", short.get("id"))
    short_title = short.get("title", "").lower()
    for video in videos:
        if video.get("title", "").lower() == short_title:
            return video
    return None
