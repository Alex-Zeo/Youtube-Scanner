import logging
import re
from datetime import datetime
from typing import Any, Dict, Optional

import requests

from youtube_scanner.models import VideoMetadata

logger = logging.getLogger(__name__)

_DURATION_RE = re.compile(
    r"PT(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?"
)


def _parse_duration(raw: str) -> Optional[int]:
    """Convert an ISO 8601 duration string to seconds."""
    match = _DURATION_RE.fullmatch(raw)
    if not match:
        return None
    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)
    return hours * 3600 + minutes * 60 + seconds


def fetch_video_data(video_id: str, api_key: str) -> Optional[VideoMetadata]:
    """Fetch and parse video metadata from the YouTube Data API."""
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,contentDetails,statistics",
        "id": video_id,
        "key": api_key,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        logger.error("YouTube API request failed for %s: %s", video_id, exc)
        return None

    try:
        payload = response.json()
    except ValueError as exc:
        logger.error("Invalid JSON for %s: %s", video_id, exc)
        return None

    items = payload.get("items")
    if not items:
        logger.warning("No data returned for video %s", video_id)
        return None

    item = items[0]
    snippet = item.get("snippet", {})
    statistics = item.get("statistics", {})
    content_details = item.get("contentDetails", {})

    def _get_field(
        container: Dict[str, Any],
        key: str,
        default: Any = None,
    ) -> Any:
        if key not in container or container[key] in (None, ""):
            logger.warning("Missing field %s for video %s", key, video_id)
            return default
        return container[key]

    title = _get_field(snippet, "title", "")
    description = _get_field(snippet, "description", "")
    publish_date_raw = _get_field(snippet, "publishedAt")
    publish_date: Optional[datetime] = None
    if publish_date_raw:
        try:
            publish_date = datetime.fromisoformat(
                publish_date_raw.replace("Z", "+00:00")
            )
        except ValueError:
            logger.warning(
                "Invalid publishedAt for video %s: %s",
                video_id,
                publish_date_raw,
            )

    duration_raw = _get_field(content_details, "duration")
    duration = _parse_duration(duration_raw) if duration_raw else None
    if duration_raw and duration is None:
        logger.warning(
            "Invalid duration for video %s: %s",
            video_id,
            duration_raw,
        )

    def _parse_int(container: Dict[str, Any], key: str) -> Optional[int]:
        raw_value = _get_field(container, key)
        if raw_value is None:
            return None
        try:
            return int(raw_value)
        except (ValueError, TypeError):
            logger.warning(
                "Invalid %s for video %s: %s",
                key,
                video_id,
                raw_value,
            )
            return None

    view_count = _parse_int(statistics, "viewCount")
    like_count = _parse_int(statistics, "likeCount")
    comment_count = _parse_int(statistics, "commentCount")

    return VideoMetadata(
        video_id=video_id,
        title=title,
        description=description,
        publish_date=publish_date,
        duration=duration,
        view_count=view_count,
        like_count=like_count,
        comment_count=comment_count,
    )
