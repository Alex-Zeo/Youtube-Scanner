"""Utilities for linking YouTube Shorts to their source videos."""

from __future__ import annotations

import logging
import re
from logging.handlers import RotatingFileHandler
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Regex to capture YouTube video IDs from typical URL formats
YOUTUBE_URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?youtu(?:\.be/|be\.com/watch\?v=)([\w-]{11})"
)


def _extract_video_id(text: str) -> Optional[str]:
    """Extract a YouTube video ID from *text* if present."""
    match = YOUTUBE_URL_RE.search(text or "")
    return match.group(1) if match else None


def map_short_to_long(
    short: Dict[str, str],
    videos: List[Dict[str, str]],
    *,
    return_source: bool = False,
) -> Optional[Dict[str, str] | Tuple[Dict[str, str], str]]:
    """Map a single short video to a full-length video.

    Parameters
    ----------
    short:
        Metadata for the short (expects ``id`` and ``title`` keys, optionally
        ``description``, ``pinned_comment`` and ``transcript``).
    videos:
        Iterable of candidate full-length video metadata dictionaries. Each
        dictionary should contain at least ``id`` and ``title`` keys and may
        include ``transcript``.
    return_source:
        When ``True`` the function returns a tuple ``(video, source)`` where
        ``source`` indicates how the match was made. When ``False`` only the
        video dictionary is returned.
    """

    logger.info("Mapping short %s", short.get("id"))

    # 1. Direct link in description
    video_id = _extract_video_id(short.get("description", ""))
    if video_id:
        for video in videos:
            if video.get("id") == video_id:
                return (video, "description") if return_source else video

    # 2. Direct link in pinned comment
    video_id = _extract_video_id(short.get("pinned_comment", ""))
    if video_id:
        for video in videos:
            if video.get("id") == video_id:
                return (video, "pinned_comment") if return_source else video

    # 3. Keyword search on titles
    short_title = (short.get("title") or "").lower()
    for video in videos:
        if (video.get("title") or "").lower() == short_title:
            return (video, "title") if return_source else video
    for video in videos:
        if short_title and short_title in (video.get("title") or "").lower():
            return (video, "title") if return_source else video

    # 4. Transcript search
    short_transcript = (short.get("transcript") or "").strip().lower()
    if short_transcript:
        for video in videos:
            transcript = (video.get("transcript") or "").lower()
            if short_transcript in transcript:
                return (video, "transcript") if return_source else video

    return (None if return_source else None)
