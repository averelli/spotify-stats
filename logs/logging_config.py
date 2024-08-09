import logging
import logging.config
import os

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR
    
class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(filename)s:%(lineno)d'
        },
    },
    'filters': {
        'error_filter': {
            '()': ErrorFilter,
        },
        "info_filter": {
            "()": InfoFilter,
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/spotify_data.log',
            'mode': 'a',
            'filters': ["info_filter"],
            'formatter': 'standard',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/spotify_data.log',
            'mode': 'a',
            'filters': ['error_filter'],
            'formatter': 'detailed',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ["info_filter"],
            'formatter': 'standard',
        },
        'console_error': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'filters': ['error_filter'],
            'formatter': 'detailed',
        },
    },
    'root': {
        'handlers': ['file', 'file_error', 'console', 'console_error'],
        'level': 'DEBUG',
        'propagate': True
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
