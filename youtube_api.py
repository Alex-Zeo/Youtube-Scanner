import logging
from typing import Any, Dict, List

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


def fetch_uploads_playlist_video_ids(channel_id: str, api_key: str) -> List[str]:
    """Return all video IDs from a channel's uploads playlist.

    This function looks up the channel's ``uploads`` playlist and iterates
    through all items using pagination. It handles quota errors from the
    YouTube Data API and transient network issues, returning the list of
    video IDs fetched so far when an error occurs.
    """
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    channel_params = {"part": "contentDetails", "id": channel_id, "key": api_key}
    try:
        response = requests.get(channel_url, params=channel_params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        try:
            error_reason = response.json()["error"]["errors"][0].get("reason")
        except Exception:  # pragma: no cover - malformed error payload
            error_reason = None
        if response.status_code == 403 and error_reason == "quotaExceeded":
            logger.error("YouTube API quota exceeded when fetching uploads playlist for %s", channel_id)
            return []
        logger.error("YouTube API returned an error for %s: %s", channel_id, exc)
        raise
    except requests.exceptions.RequestException as exc:
        logger.warning("Network issue when fetching uploads playlist for %s: %s", channel_id, exc)
        return []

    uploads_playlist_id = (
        response.json()
        .get("items", [{}])[0]
        .get("contentDetails", {})
        .get("relatedPlaylists", {})
        .get("uploads")
    )
    if not uploads_playlist_id:
        logger.warning("No uploads playlist found for %s", channel_id)
        return []

    video_ids: List[str] = []
    playlist_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": "contentDetails",
        "playlistId": uploads_playlist_id,
        "maxResults": 50,
        "key": api_key,
    }
    while True:
        try:
            pl_response = requests.get(playlist_url, params=params, timeout=10)
            pl_response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            try:
                error_reason = pl_response.json()["error"]["errors"][0].get("reason")
            except Exception:  # pragma: no cover - malformed error payload
                error_reason = None
            if pl_response.status_code == 403 and error_reason == "quotaExceeded":
                logger.error("YouTube API quota exceeded when fetching videos for %s", channel_id)
                return video_ids
            logger.error("YouTube API returned an error for %s: %s", channel_id, exc)
            raise
        except requests.exceptions.RequestException as exc:
            logger.warning("Network issue when fetching playlist items for %s: %s", channel_id, exc)
            return video_ids

        data = pl_response.json()
        for item in data.get("items", []):
            vid = item.get("contentDetails", {}).get("videoId")
            if vid:
                video_ids.append(vid)

        next_token = data.get("nextPageToken")
        if not next_token:
            break
        params["pageToken"] = next_token

    return video_ids
