from youtube_scanner.channel_fetcher import fetch_uploads


def test_fetch_uploads_logs_and_returns_list(caplog):
    with caplog.at_level("INFO"):
        result = fetch_uploads("CHANNEL_ID")
    assert result == []
    assert "Fetching uploads for channel CHANNEL_ID" in caplog.text
