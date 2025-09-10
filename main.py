import logging
import sys
from pathlib import Path

from process_utils import run_command
from youtube_api import fetch_video_data

sys.path.append(str(Path(__file__).resolve().parent / "src"))
from youtube_scanner.logging_config import setup_logging  # noqa: E402

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    logger.info("Demo starting")
    try:
        fetch_video_data("dQw4w9WgXcQ", "INVALID_API_KEY")
    except Exception as exc:
        logger.error("Failed to fetch video data: %s", exc)

    try:
        run_command(["echo", "Hello"])
    except Exception as exc:
        logger.error("Command execution failed: %s", exc)


if __name__ == "__main__":
    main()
