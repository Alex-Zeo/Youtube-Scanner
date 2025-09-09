from youtube_scanner.video_classifier import is_short


def test_is_short_classifies_videos_correctly(caplog):
    with caplog.at_level("DEBUG"):
        assert is_short({"duration": 30})
        assert not is_short({"duration": 120})
    assert "Classifying video with duration 30" in caplog.text
