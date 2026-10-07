"""Guard against a second ``youtube_scanner`` tree shadowing the packaged one.

Main went red in 2025-09 because merges left divergent copies under ``./`` and
``./src``; ``conftest.py`` puts ``src`` first, so names defined only in the root
copy vanished at import time. Each row is a public name some caller depends on.
"""

import importlib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC_PACKAGE = ROOT / "src" / "youtube_scanner"

PUBLIC_API = [
    ("channel_fetcher", "fetch_uploads"),
    ("channel_fetcher", "fetch_channel_videos"),
    ("metadata_collector", "collect_metadata"),
    ("models", "ChannelConfig"),
    ("models", "ShortMapping"),
    ("models", "VideoMetadata"),
    ("scheduler", "schedule_monthly"),
    ("scheduler", "run_channel_scan"),
    ("scheduler", "start"),
    ("scheduler", "stop"),
    ("short_mapper", "map_short_to_long"),
    ("short_mapper", "map_shorts_to_full"),
    ("storage", "save_results"),
    ("storage", "get_last_run"),
    ("storage", "update_last_run"),
    ("storage", "append_video_metadata"),
    ("storage", "load_video_metadata"),
    ("storage", "append_short_mappings"),
    ("storage", "load_short_mappings"),
    ("transcript_fetcher", "fetch_transcript"),
    ("video_classifier", "classify_video"),
    ("video_classifier", "classify_duration"),
    ("video_classifier", "is_short"),
]


def test_single_package_tree():
    assert not (ROOT / "youtube_scanner").exists()


@pytest.mark.parametrize("module,name", PUBLIC_API)
def test_public_api_resolves_from_src(module, name):
    mod = importlib.import_module(f"youtube_scanner.{module}")
    assert Path(mod.__file__).resolve().parent == SRC_PACKAGE
    assert hasattr(mod, name), f"youtube_scanner.{module} lacks {name}"
