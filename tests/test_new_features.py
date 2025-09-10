import json

from youtube_scanner.channel_fetcher import fetch_uploads
from youtube_scanner.metadata_collector import collect_metadata
from youtube_scanner.shorts_mapper import map_shorts_to_full
from youtube_scanner.transcript_fetcher import fetch_transcript
from youtube_scanner.storage import save_results


def test_fetch_uploads_returns_empty_list_and_logs(caplog):
    with caplog.at_level("INFO"):
        result = fetch_uploads("CHANNEL_ID")
    assert result == []
    assert "Fetching uploads for channel CHANNEL_ID" in caplog.text


def test_collect_metadata_returns_empty_dict_and_logs(caplog):
    with caplog.at_level("INFO"):
        result = collect_metadata("VIDEO_ID")
    assert result == {}
    assert "Collecting metadata for video VIDEO_ID" in caplog.text


def test_map_shorts_to_full_returns_empty_mapping_and_logs(caplog):
    shorts = ["s1", "s2"]
    full_videos = ["v1", "v2"]
    with caplog.at_level("INFO"):
        mapping = map_shorts_to_full(shorts, full_videos)
    assert mapping == {}
    assert "Mapping 2 shorts to full videos" in caplog.text


def test_fetch_transcript_returns_empty_list_and_logs(caplog):
    with caplog.at_level("INFO"):
        transcript = fetch_transcript("VIDEO_ID")
    assert transcript == []
    assert "Fetching transcript for VIDEO_ID" in caplog.text


def test_save_results_writes_json(tmp_path):
    data = {"a": 1}
    filename = tmp_path / "out.json"
    save_results(data, filename=str(filename))
    assert filename.exists()
    assert json.loads(filename.read_text()) == data
