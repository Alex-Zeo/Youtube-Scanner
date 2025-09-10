from youtube_scanner.video_classifier import classify_duration, is_short


def test_classify_duration_and_is_short(caplog):
    with caplog.at_level("DEBUG"):
        assert classify_duration(30) == "short"
        assert classify_duration(120) == "long"
        assert is_short({"duration": 30})
        assert not is_short({"duration": 120})
    assert "Classifying video with duration 30" in caplog.text
