import pytest
from youtube_transcript_api import TranscriptsDisabled
from requests import exceptions as requests_exceptions

from youtube_scanner.transcript_fetcher import fetch_transcript


def test_fetch_transcript_success(monkeypatch):
    sample = [{"text": "Hello"}, {"text": "World"}]
    monkeypatch.setattr(
        "youtube_scanner.transcript_fetcher.YouTubeTranscriptApi.fetch",
        lambda self, video_id, languages=None: sample,
    )
    result = fetch_transcript("vid")
    assert result == ["Hello", "World"]


def test_fetch_transcript_disabled(monkeypatch, caplog):
    def _raise(self, video_id, languages=None):
        raise TranscriptsDisabled("disabled")

    monkeypatch.setattr(
        "youtube_scanner.transcript_fetcher.YouTubeTranscriptApi.fetch",
        _raise,
    )
    with caplog.at_level("WARNING"):
        result = fetch_transcript("vid")
    assert result == []
    assert "Transcripts disabled" in caplog.text


def test_fetch_transcript_network_error(monkeypatch, caplog):
    def _raise(self, video_id, languages=None):
        raise requests_exceptions.RequestException("boom")

    monkeypatch.setattr(
        "youtube_scanner.transcript_fetcher.YouTubeTranscriptApi.fetch",
        _raise,
    )
    with caplog.at_level("WARNING"):
        result = fetch_transcript("vid")
    assert result == []
    assert "Network error retrieving transcript" in caplog.text
