from datetime import datetime, timezone
from typing import Any

import youtube_api
from youtube_scanner.models import VideoMetadata


class MockResponse:
    def __init__(self, payload: dict[str, Any]):
        self._payload = payload

    def raise_for_status(self):
        pass

    def json(self):
        return self._payload


def test_fetch_video_data_parses_response(monkeypatch):
    payload = {
        "items": [
            {
                "id": "abc123",
                "snippet": {
                    "title": "My Video",
                    "description": "Desc",
                    "publishedAt": "2024-01-01T00:00:00Z",
                },
                "contentDetails": {"duration": "PT1M5S"},
                "statistics": {
                    "viewCount": "100",
                    "likeCount": "5",
                    "commentCount": "2",
                },
            }
        ]
    }

    def fake_get(url: str, params: dict[str, Any], timeout: int):
        return MockResponse(payload)

    monkeypatch.setattr(youtube_api.requests, "get", fake_get)

    metadata = youtube_api.fetch_video_data("abc123", "KEY")
    assert isinstance(metadata, VideoMetadata)
    assert metadata.title == "My Video"
    assert metadata.description == "Desc"
    expected_date = datetime(2024, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert metadata.publish_date == expected_date
    assert metadata.duration == 65
    assert metadata.view_count == 100
    assert metadata.like_count == 5
    assert metadata.comment_count == 2


def test_fetch_video_data_missing_fields(monkeypatch, caplog):
    payload = {
        "items": [
            {
                "id": "abc123",
                "snippet": {},
                "statistics": {},
                "contentDetails": {},
            }
        ]
    }

    def fake_get(url: str, params: dict[str, Any], timeout: int):
        return MockResponse(payload)

    monkeypatch.setattr(youtube_api.requests, "get", fake_get)

    with caplog.at_level("WARNING"):
        metadata = youtube_api.fetch_video_data("abc123", "KEY")

    assert isinstance(metadata, VideoMetadata)
    assert metadata.title == ""
    assert metadata.publish_date is None
    assert "Missing field title" in caplog.text
