import logging
import logging.config
from youtube_api import fetch_video_data
from process_utils import run_command

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'app.log',
            'encoding': 'utf8'
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file']
    }
}

def main():
    logging.config.dictConfig(LOGGING_CONFIG)
    try:
        fetch_video_data('dQw4w9WgXcQ', 'INVALID_API_KEY')
    except Exception:
        pass

    try:
        run_command(['echo', 'Hello'])
    except Exception:
        pass

if __name__ == '__main__':
    main()
