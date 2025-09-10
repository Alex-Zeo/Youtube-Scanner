import requests
from unittest.mock import Mock, patch

from youtube_api import fetch_uploads_playlist_video_ids


def test_fetch_uploads_playlist_video_ids_handles_pagination():
    channel_resp = Mock()
    channel_resp.json.return_value = {
        "items": [{"contentDetails": {"relatedPlaylists": {"uploads": "UPLOADS_ID"}}}]
    }
    channel_resp.raise_for_status.return_value = None

    first_page = Mock()
    first_page.json.return_value = {
        "items": [
            {"contentDetails": {"videoId": "id1"}},
            {"contentDetails": {"videoId": "id2"}},
        ],
        "nextPageToken": "TOKEN",
    }
    first_page.raise_for_status.return_value = None

    second_page = Mock()
    second_page.json.return_value = {
        "items": [{"contentDetails": {"videoId": "id3"}}]
    }
    second_page.raise_for_status.return_value = None

    with patch("youtube_api.requests.get", side_effect=[channel_resp, first_page, second_page]):
        result = fetch_uploads_playlist_video_ids("CHANNEL", "KEY")

    assert result == ["id1", "id2", "id3"]


def test_fetch_uploads_playlist_video_ids_quota_exceeded(caplog):
    resp = Mock()
    resp.status_code = 403
    resp.json.return_value = {"error": {"errors": [{"reason": "quotaExceeded"}]}}
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError(response=resp)

    with patch("youtube_api.requests.get", return_value=resp):
        with caplog.at_level("ERROR"):
            result = fetch_uploads_playlist_video_ids("CHANNEL", "KEY")

    assert result == []
    assert "quota exceeded" in caplog.text.lower()


def test_fetch_uploads_playlist_video_ids_network_issue(caplog):
    with patch("youtube_api.requests.get", side_effect=requests.exceptions.RequestException("boom")):
        with caplog.at_level("WARNING"):
            result = fetch_uploads_playlist_video_ids("CHANNEL", "KEY")

    assert result == []
    assert "network issue" in caplog.text.lower()
