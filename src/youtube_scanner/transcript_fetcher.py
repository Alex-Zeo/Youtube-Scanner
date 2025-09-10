"""Retrieve transcripts via the YouTube caption API or
youtube-transcript-api."""

import logging
from typing import List

logger = logging.getLogger(__name__)


def fetch_transcript(video_id: str) -> List[str]:
    """Placeholder for retrieving a video's transcript."""
    logger.info("Fetching transcript for %s", video_id)
    # TODO: Implement transcript retrieval
    return []
