from __future__ import annotations

"""Data models for the Youtube Scanner project.

This module defines lightweight data containers used throughout the
application.  Each dataclass provides helpers for serialising to and from
common formats such as dictionaries, JSON strings and CSV rows.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Optional
import json


@dataclass
class VideoMetadata:
    """Metadata about a YouTube video.

    Attributes:
        video_id: Unique identifier for the video.
        title: Video title.
        description: Textual description of the video.
        publish_date: When the video was published.
        view_count: Number of views the video has received.
        like_count: Number of likes for the video.
        comment_count: Number of comments on the video.
        duration: Length of the video in seconds.
        is_short: True if the video is considered a YouTube Short.
    """

    video_id: str
    title: str
    description: str = ""
    publish_date: Optional[datetime] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    duration: Optional[int] = None
    is_short: bool = False

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.publish_date is not None:
            data["publish_date"] = self.publish_date.isoformat()
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "VideoMetadata":
        data = dict(data)
        publish_date = data.get("publish_date")
        if publish_date is not None and not isinstance(publish_date, datetime):
            data["publish_date"] = datetime.fromisoformat(publish_date)
        return cls(**data)

    @classmethod
    def from_json(cls, raw: str) -> "VideoMetadata":
        return cls.from_dict(json.loads(raw))

    # CSV helpers -------------------------------------------------------
    @classmethod
    def csv_headers(cls) -> list[str]:
        return [
            "video_id",
            "title",
            "description",
            "publish_date",
            "view_count",
            "like_count",
            "comment_count",
            "duration",
            "is_short",
        ]

    def to_csv_row(self) -> list[str]:
        data = self.to_dict()
        return ["" if data.get(h) is None else str(data.get(h)) for h in self.csv_headers()]

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "VideoMetadata":
        data: Dict[str, Any] = dict(row)
        if data.get("publish_date"):
            data["publish_date"] = datetime.fromisoformat(data["publish_date"])
        for key in ["view_count", "like_count", "comment_count", "duration"]:
            if data.get(key):
                data[key] = int(data[key])
        if data.get("is_short"):
            data["is_short"] = data["is_short"].lower() in {"1", "true", "yes"}
        return cls(**data)


@dataclass
class ShortMapping:
    """Links a Short to its long-form video counterpart."""

    short_video_id: str
    full_video_id: Optional[str] = None
    relation_source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ShortMapping":
        return cls(**data)

    @classmethod
    def from_json(cls, raw: str) -> "ShortMapping":
        return cls.from_dict(json.loads(raw))

    @classmethod
    def csv_headers(cls) -> list[str]:
        return ["short_video_id", "full_video_id", "relation_source"]

    def to_csv_row(self) -> list[str]:
        data = self.to_dict()
        return ["" if data.get(h) is None else str(data.get(h)) for h in self.csv_headers()]

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "ShortMapping":
        return cls(**row)


@dataclass
class ChannelConfig:
    """Configuration describing a YouTube channel to scan."""

    channel_id: str
    name: str
    category: Optional[str] = None
    short_view_threshold: int = 50_000
    top_n_shorts: int = 20

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChannelConfig":
        return cls(**data)

    @classmethod
    def from_json(cls, raw: str) -> "ChannelConfig":
        return cls.from_dict(json.loads(raw))

    @classmethod
    def csv_headers(cls) -> list[str]:
        return [
            "channel_id",
            "name",
            "category",
            "short_view_threshold",
            "top_n_shorts",
        ]

    def to_csv_row(self) -> list[str]:
        data = self.to_dict()
        return ["" if data.get(h) is None else str(data.get(h)) for h in self.csv_headers()]

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "ChannelConfig":
        data: Dict[str, Any] = dict(row)
        if data.get("short_view_threshold"):
            data["short_view_threshold"] = int(data["short_view_threshold"])
        if data.get("top_n_shorts"):
            data["top_n_shorts"] = int(data["top_n_shorts"])
        return cls(**data)
