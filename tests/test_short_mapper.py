from youtube_scanner.short_mapper import map_short_to_long


def test_map_short_to_long(caplog):
    short = {"id": "abc123", "title": "Short video"}
    videos = [
        {"id": "long1", "title": "Short Video"},
        {"id": "long2", "title": "Another Video"},
    ]
    with caplog.at_level("INFO"):
        result = map_short_to_long(short, videos)
    assert result == videos[0]
    assert "Mapping short abc123" in caplog.text


def test_map_short_to_long_no_match():
    short = {"id": "abc123", "title": "Short video"}
    videos = [{"id": "long1", "title": "Different"}]
    assert map_short_to_long(short, videos) is None
