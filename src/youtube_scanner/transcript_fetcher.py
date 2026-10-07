"""Retrieve transcripts using the YouTube caption API or youtube-transcript-api."""

from typing import List
import logging
from logging.handlers import RotatingFileHandler

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript,
    VideoUnavailable,
)
from requests import exceptions as requests_exceptions

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = RotatingFileHandler("youtube_scanner.log", maxBytes=1_000_000, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

def fetch_transcript(video_id: str) -> List[str]:
    """Fetch the transcript for ``video_id``.

    This uses :mod:`youtube_transcript_api` to retrieve either an official
    transcript or an auto-generated one when available.  If transcripts are
    disabled or a network error occurs, a warning is logged and an empty list
    is returned.
    """

    logger.info("Fetching transcript for %s", video_id)

    try:
        entries = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
        return [entry["text"] for entry in entries if entry.get("text")]
    except TranscriptsDisabled:
        logger.warning("Transcripts disabled for %s", video_id)
    except (NoTranscriptFound, CouldNotRetrieveTranscript, VideoUnavailable) as exc:
        logger.warning("No transcript available for %s: %s", video_id, exc)
    except requests_exceptions.RequestException as exc:
        logger.warning("Network error retrieving transcript for %s: %s", video_id, exc)
    except Exception as exc:  # pragma: no cover - unexpected errors
        logger.warning("Failed to fetch transcript for %s: %s", video_id, exc)
    return []
