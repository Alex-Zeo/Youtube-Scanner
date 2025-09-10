# Logging Conventions

- Each module defines a module-level logger using `logging.getLogger(__name__)` and
  never adds its own handlers.
- The root logger is configured once via
  `youtube_scanner.logging_config.setup_logging()`.
- Console output logs messages at `INFO` level and above.
- Debug information is written to a rotating file `youtube_scanner.log` using the
  same formatter, which includes:
  - timestamp
  - module name
  - log level
  - log message
- Wrap external API calls and subprocesses in `try/except` blocks.
  - Log recoverable issues with `logger.warning`.
  - Log failures that abort processing with `logger.error` and re-raise when needed.

Example entrypoint:

```python
import logging
from youtube_scanner.logging_config import setup_logging

logger = logging.getLogger(__name__)

def main() -> None:
    setup_logging()
    logger.info("Scanner starting")

if __name__ == "__main__":
    main()
```
