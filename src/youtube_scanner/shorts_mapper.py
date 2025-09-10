"""Map Shorts to full videos via descriptions, comments, search, and transcripts."""

from typing import Dict, List
import logging
from logging.handlers import RotatingFileHandler

from .short_mapper import map_short_to_long

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)


def map_shorts_to_full(
    shorts: List[Dict[str, str]],
    full_videos: List[Dict[str, str]],
) -> Dict[str, Dict[str, str]]:
    """Map a list of shorts to their corresponding full videos.

    Parameters
    ----------
    shorts:
        List of short video metadata dictionaries. Each dictionary should at
        minimum contain an ``id`` key and may include ``title``, ``description``,
        ``pinned_comment`` and ``transcript``.
    full_videos:
        List of candidate full-length video metadata dictionaries.

    Returns
    -------
    dict
        Mapping of short IDs to dictionaries containing the matched full video
        ID and the relation ``source`` that triggered the match.
    """
    logger.info("Mapping %d shorts to full videos", len(shorts))
    mapping: Dict[str, Dict[str, str]] = {}
    for short in shorts:
        result = map_short_to_long(short, full_videos, return_source=True)
        if result:
            video, source = result
            mapping[short["id"]] = {"video_id": video["id"], "source": source}
    return mapping
