"""Compatibility layer for data models.

The canonical dataclass definitions live in ``src.youtube_scanner.models``.
This module re-exports the most commonly used models so that the rest of the
codebase can simply import from ``youtube_scanner``.
"""

from src.youtube_scanner.models import ChannelConfig, ShortMapping, VideoMetadata

__all__ = ["ChannelConfig", "ShortMapping", "VideoMetadata"]
