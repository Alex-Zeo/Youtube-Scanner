import logging
import subprocess
from typing import List

logger = logging.getLogger(__name__)


def run_command(cmd: List[str]) -> str:
    """Run an external command and return its output."""
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return result.stdout
    except FileNotFoundError as exc:
        logger.warning("Command not found: %s", exc)
        return ""
    except subprocess.CalledProcessError as exc:
        logger.error("Command '%s' failed with %s", " ".join(cmd), exc)
        raise
