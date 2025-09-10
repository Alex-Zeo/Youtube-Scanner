"""Fetch uploads using the YouTube Data API."""

from typing import Dict, List, Any
import logging
from logging.handlers import RotatingFileHandler

import requests

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

API_URL = "https://www.googleapis.com/youtube/v3/search"


def fetch_channel_videos(api_key: str, channel_id: str) -> Dict[str, Any]:
    """Fetch videos for a channel using the YouTube Data API.

    Parameters
    ----------
    api_key:
        API key used for authenticating with the YouTube Data API.
    channel_id:
        Identifier of the YouTube channel whose videos should be fetched.

    Returns
    -------
    dict
        JSON response from the API containing video information.
    """
    logger.info("Fetching channel videos for %s", channel_id)
    params = {
        "part": "snippet",
        "channelId": channel_id,
        "maxResults": 50,
        "order": "date",
        "key": api_key,
    }
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_uploads(channel_id: str) -> List[str]:
    """Placeholder retained for backward compatibility."""
    logger.info("Fetching uploads for channel %s", channel_id)
    return []
