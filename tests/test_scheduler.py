from youtube_scanner import scheduler


def test_run_channel_scan_updates_storage(monkeypatch):
    calls = []

    def fake_fetch(api_key, channel_id):
        calls.append((api_key, channel_id))
        return {}

    store = {}

    monkeypatch.setattr(scheduler.channel_fetcher, "fetch_channel_videos", fake_fetch)
    monkeypatch.setattr(scheduler.storage, "get_last_run", lambda cid: store.get(cid))
    monkeypatch.setattr(scheduler.storage, "update_last_run", lambda cid, ts: store.__setitem__(cid, ts))

    scheduler.API_KEY = "key"
    scheduler.CHANNELS = ["c1"]
    scheduler.run_channel_scan()

    assert calls == [("key", "c1")]
    assert "c1" in store


def test_start_schedules_monthly_job(monkeypatch):
    scheduler.CHANNELS = []
    sched = scheduler.start()
    try:
        jobs = sched.get_jobs()
        assert len(jobs) == 1
        assert "day='1'" in str(jobs[0].trigger)
    finally:
        scheduler.stop(sched)
