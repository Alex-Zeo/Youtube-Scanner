from __future__ import annotations

"""Persistence helpers for ``VideoMetadata`` and ``ShortMapping`` collections.

The functions in this module can read and write the project data models either
as JSON files or in a lightweight SQLite database.  The storage backend is
chosen based on the file extension: ``.json`` for JSON files and ``.sqlite`` or
``.db`` for SQLite databases.
"""

from dataclasses import asdict
from datetime import datetime
import json
import sqlite3
from pathlib import Path
from typing import Iterable, List

from .models import ShortMapping, VideoMetadata


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _is_sqlite(path: Path) -> bool:
    """Return ``True`` if the path points to an SQLite database."""
    return path.suffix in {".sqlite", ".db"}


# ---------------------------------------------------------------------------
# Video metadata
# ---------------------------------------------------------------------------

def load_video_metadata(filename: str | Path) -> List[VideoMetadata]:
    """Load all stored :class:`VideoMetadata` records from ``filename``."""
    path = Path(filename)
    if _is_sqlite(path):
        conn = sqlite3.connect(path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS video_metadata (
                video_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                publish_date TEXT,
                view_count INTEGER,
                like_count INTEGER,
                comment_count INTEGER,
                duration INTEGER,
                is_short INTEGER
            )
            """
        )
        rows = conn.execute(
            "SELECT video_id, title, description, publish_date, view_count, like_count, comment_count, duration, is_short FROM video_metadata"
        ).fetchall()
        conn.close()
        records: List[VideoMetadata] = []
        for row in rows:
            publish_date = datetime.fromisoformat(row[3]) if row[3] else None
            records.append(
                VideoMetadata(
                    video_id=row[0],
                    title=row[1],
                    description=row[2] or "",
                    publish_date=publish_date,
                    view_count=row[4],
                    like_count=row[5],
                    comment_count=row[6],
                    duration=row[7],
                    is_short=bool(row[8]),
                )
            )
        return records

    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
    else:
        raw = []
    return [VideoMetadata.from_dict(item) for item in raw]


def append_video_metadata(records: Iterable[VideoMetadata], filename: str | Path) -> None:
    """Append ``records`` to the video metadata collection at ``filename``."""
    path = Path(filename)
    if _is_sqlite(path):
        conn = sqlite3.connect(path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS video_metadata (
                video_id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                publish_date TEXT,
                view_count INTEGER,
                like_count INTEGER,
                comment_count INTEGER,
                duration INTEGER,
                is_short INTEGER
            )
            """
        )
        data = [
            (
                r.video_id,
                r.title,
                r.description,
                r.publish_date.isoformat() if r.publish_date else None,
                r.view_count,
                r.like_count,
                r.comment_count,
                r.duration,
                int(r.is_short),
            )
            for r in records
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO video_metadata VALUES (?,?,?,?,?,?,?,?,?)",
            data,
        )
        conn.commit()
        conn.close()
        return

    existing = load_video_metadata(path)
    existing.extend(records)
    with path.open("w", encoding="utf-8") as fh:
        json.dump([asdict(r) for r in existing], fh, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Short mappings
# ---------------------------------------------------------------------------

def load_short_mappings(filename: str | Path) -> List[ShortMapping]:
    """Load all stored :class:`ShortMapping` records from ``filename``."""
    path = Path(filename)
    if _is_sqlite(path):
        conn = sqlite3.connect(path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS short_mappings (
                short_video_id TEXT PRIMARY KEY,
                full_video_id TEXT,
                relation_source TEXT
            )
            """
        )
        rows = conn.execute(
            "SELECT short_video_id, full_video_id, relation_source FROM short_mappings"
        ).fetchall()
        conn.close()
        return [
            ShortMapping(
                short_video_id=row[0],
                full_video_id=row[1],
                relation_source=row[2],
            )
            for row in rows
        ]

    if path.exists():
        with path.open("r", encoding="utf-8") as fh:
            raw = json.load(fh)
    else:
        raw = []
    return [ShortMapping.from_dict(item) for item in raw]


def append_short_mappings(records: Iterable[ShortMapping], filename: str | Path) -> None:
    """Append ``records`` to the short mapping collection at ``filename``."""
    path = Path(filename)
    if _is_sqlite(path):
        conn = sqlite3.connect(path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS short_mappings (
                short_video_id TEXT PRIMARY KEY,
                full_video_id TEXT,
                relation_source TEXT
            )
            """
        )
        data = [
            (r.short_video_id, r.full_video_id, r.relation_source) for r in records
        ]
        conn.executemany(
            "INSERT OR REPLACE INTO short_mappings VALUES (?,?,?)",
            data,
        )
        conn.commit()
        conn.close()
        return

    existing = load_short_mappings(path)
    existing.extend(records)
    with path.open("w", encoding="utf-8") as fh:
        json.dump([asdict(r) for r in existing], fh, ensure_ascii=False, indent=2)


__all__ = [
    "append_short_mappings",
    "append_video_metadata",
    "load_short_mappings",
    "load_video_metadata",
]
