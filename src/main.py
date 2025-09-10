"""Executable entry point for coordinating YouTube Scanner modules."""

import logging

from youtube_scanner.channel_fetcher import fetch_uploads
from youtube_scanner.logging_config import setup_logging
from youtube_scanner.metadata_collector import collect_metadata
from youtube_scanner.scheduler import schedule_monthly
from youtube_scanner.shorts_mapper import map_shorts_to_full
from youtube_scanner.storage import save_results
from youtube_scanner.transcript_fetcher import fetch_transcript
from youtube_scanner.video_classifier import classify_video

logger = logging.getLogger(__name__)


def main() -> None:
    """Coordinate scanning workflow."""
    setup_logging()
    channel_id = "UC_x5XG1OV2P6uZZ5FSM9Ttw"  # Placeholder channel ID
    uploads = fetch_uploads(channel_id)
    shorts, longs = [], []

    for video_id in uploads:
        metadata = collect_metadata(video_id)
        duration = metadata.get("duration", 0)
        classification = classify_video(duration)
        if classification == "short":
            shorts.append(video_id)
        else:
            longs.append(video_id)
        fetch_transcript(video_id)

    mapping = map_shorts_to_full(shorts, longs)
    save_results({"mapping": mapping})
    schedule_monthly(main)
    logger.info("Scan complete")


if __name__ == "__main__":
    main()
