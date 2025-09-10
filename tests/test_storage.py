from datetime import datetime

from youtube_scanner import storage


def test_update_and_get_last_run(tmp_path, monkeypatch):
    file = tmp_path / "last_run.json"
    monkeypatch.setattr(storage, "_STORAGE_FILE", file)
    ts = datetime(2024, 1, 1)
    storage.update_last_run("channel1", ts)
    assert storage.get_last_run("channel1") == ts
