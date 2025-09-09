import logging
from typing import Any, Dict
import requests

logger = logging.getLogger(__name__)


def fetch_channel_videos(api_key: str, channel_id: str) -> Dict[str, Any]:
    """Fetch videos for a given channel using the YouTube Data API."""
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 50,
        "key": api_key,
    }
    logger.info("Fetching channel videos for %s", channel_id)
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
