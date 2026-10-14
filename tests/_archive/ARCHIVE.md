# Archived tests

Tests in this directory are kept out of pytest collection by `collect_ignore = ["_archive"]` in `tests/conftest.py`. Each row was accepted for archive by Judge B (ruling on the test-archive audit packet for Youtube-Scanner, audit head 437df3cdc6ce8d6c3e3b11e991f3c6439195a9d0). Restore a file with its one-line command from the repo root; pytest collects it again at once.

| Test id | Original file:line | Reason | Restore |
|---|---|---|---|
| `tests/test_short_mapper.py::test_map_short_to_long` | tests/test_short_mapper.py:4 | Judge B ruling, accepted row (weight 1): map_short_to_long (src/youtube_scanner/short_mapper.py:16-23) has no call site on main or on PR 21; src/main.py:38 calls the different map_shorts_to_full. | `git mv tests/_archive/test_short_mapper.py tests/test_short_mapper.py` |
| `tests/test_short_mapper.py::test_map_short_to_long_no_match` | tests/test_short_mapper.py:16 | Judge B ruling, accepted row (weight 1): same function and trace as the match row, no caller in either tree. | `git mv tests/_archive/test_short_mapper.py tests/test_short_mapper.py` |
