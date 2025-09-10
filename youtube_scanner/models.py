"""Data models for the Youtube Scanner project."""

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class VideoMetadata:
    """Metadata about a YouTube video."""

    video_id: str
    title: str
    description: str = ""
    publish_date: Optional[datetime] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    duration: Optional[int] = None
    is_short: bool = False

    # Serialisation helpers -------------------------------------------------
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

    # CSV helpers -----------------------------------------------------------
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
        row: list[str] = []
        for header in self.csv_headers():
            value = "" if data.get(header) is None else str(data.get(header))
            row.append(value)
        return row

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
