import logging
from typing import Any, Dict

import requests

logger = logging.getLogger(__name__)


def fetch_video_data(video_id: str, api_key: str) -> Dict[str, Any]:
    """Fetch video metadata from the YouTube Data API."""
    url = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': video_id,
        'key': api_key,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        logger.error("YouTube API returned an error for %s: %s", video_id, exc)
        raise
    except requests.exceptions.RequestException as exc:
        logger.warning("Network issue when fetching %s: %s", video_id, exc)
        return {}

    try:
        return response.json()
    except ValueError as exc:
        logger.warning("Invalid JSON for %s: %s", video_id, exc)
        return {}
