# Logging Conventions

- Each module defines a module-level logger using `logging.getLogger(__name__)`.
- The root logger is configured in `main.py` via `logging.config.dictConfig`.
- Console output logs messages at `INFO` level and above.
- Debug information is written to `app.log` using the same formatter, which includes:
  - timestamp
  - module name
  - log level
  - log message
- Wrap external API calls and subprocesses in `try/except` blocks.
  - Log recoverable issues with `logger.warning`.
  - Log failures that abort processing with `logger.error` and re-raise when needed.
