from youtube_scanner.video_classifier import classify_video, is_short


def test_is_short_and_classify_video(caplog):
    with caplog.at_level("DEBUG"):
        assert is_short({"duration": 30})
        assert not is_short({"duration": 120})
        assert classify_video(30) == "short"
        assert classify_video(120) == "long"
    assert "Classifying video with duration 30" in caplog.text
    assert "Classified duration 30 as short" in caplog.text
