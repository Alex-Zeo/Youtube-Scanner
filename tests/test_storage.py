from datetime import datetime

from youtube_scanner import storage


def test_update_and_get_last_run(tmp_path, monkeypatch):
    file = tmp_path / "last_run.json"
    monkeypatch.setattr(storage, "_STORAGE_FILE", file)
    ts = datetime(2024, 1, 1)
    storage.update_last_run("channel1", ts)
    assert storage.get_last_run("channel1") == ts
import pytest

from youtube_scanner.models import ShortMapping, VideoMetadata
from youtube_scanner.storage import (
    append_short_mappings,
    append_video_metadata,
    load_short_mappings,
    load_video_metadata,
)


@pytest.mark.parametrize("suffix", ["json", "sqlite"])
def test_video_metadata_roundtrip(tmp_path, suffix):
    path = tmp_path / f"videos.{suffix}"
    v1 = VideoMetadata(video_id="a", title="A")
    v2 = VideoMetadata(video_id="b", title="B", is_short=True)
    append_video_metadata([v1], path)
    append_video_metadata([v2], path)
    loaded = load_video_metadata(path)
    loaded_sorted = sorted(loaded, key=lambda v: v.video_id)
    assert loaded_sorted == [v1, v2]


@pytest.mark.parametrize("suffix", ["json", "sqlite"])
def test_short_mapping_roundtrip(tmp_path, suffix):
    path = tmp_path / f"shorts.{suffix}"
    m1 = ShortMapping(short_video_id="s1", full_video_id="f1")
    m2 = ShortMapping(short_video_id="s2", relation_source="desc")
    append_short_mappings([m1], path)
    append_short_mappings([m2], path)
    loaded = load_short_mappings(path)
    loaded_sorted = sorted(loaded, key=lambda m: m.short_video_id)
    assert loaded_sorted == [m1, m2]