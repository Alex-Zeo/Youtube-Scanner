"""Central logging configuration for Youtube Scanner.

This module exposes :func:`setup_logging` which configures the logging
system using :func:`logging.config.dictConfig`.
"""

from __future__ import annotations

import logging.config
from logging.handlers import RotatingFileHandler  # noqa: F401

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "filename": "youtube_scanner.log",
            "maxBytes": 1_000_000,
            "backupCount": 3,
            "encoding": "utf8",
        },
    },
    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}


def setup_logging() -> None:
    """Configure logging using :data:`LOGGING_CONFIG`."""
    logging.config.dictConfig(LOGGING_CONFIG)
