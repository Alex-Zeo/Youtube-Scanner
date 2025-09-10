from youtube_scanner.video_classifier import classify_video


def test_classify_video_labels_videos_correctly(caplog):
    with caplog.at_level("INFO"):
        assert classify_video(30) == "short"
        assert classify_video(120) == "long"
    assert "Classified duration 30 as short" in caplog.text
