from unittest.mock import Mock, patch

from youtube_scanner.channel_fetcher import fetch_channel_videos


def test_fetch_channel_videos_makes_request_and_returns_json(caplog):
    mock_json = {"items": ["video1", "video2"]}
    with patch("youtube_scanner.channel_fetcher.requests.get") as mock_get:
        mock_resp = Mock()
        mock_resp.json.return_value = mock_json
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp
        with caplog.at_level("INFO"):
            result = fetch_channel_videos("API_KEY", "CHANNEL_ID")
    assert result == mock_json
    assert "Fetching channel videos for CHANNEL_ID" in caplog.text
    mock_get.assert_called_once()
