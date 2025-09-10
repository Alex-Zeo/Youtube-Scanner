"""Persistence helpers for VideoMetadata and ShortMapping.

This module simply re-exports the storage helpers from the top-level
``youtube_scanner.storage`` package.  It exists for backward compatibility with
older imports that referenced ``src.youtube_scanner.storage``.
"""

from youtube_scanner.storage import (
    append_short_mappings,
    append_video_metadata,
    load_short_mappings,
    load_video_metadata,
)

__all__ = [
    "append_short_mappings",
    "append_video_metadata",
    "load_short_mappings",
    "load_video_metadata",
]
