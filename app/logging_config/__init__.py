"""This file sets up the logging behavior of the app"""
import os
import logging
import logging.config
from app.config import Config

def logging_setup():
    """Logging Setup"""
    logdir = Config.LOG_DIR
    # make a directory if it doesn't exist
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    # this loads the log configuration
    logging.config.dictConfig(LOGGING_CONFIG)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'data_view': {
            'format': '%(message)s'
        },

    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file.handler.information': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.abspath(os.path.join(Config.LOG_DIR, 'information.log')),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.default_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.abspath(os.path.join(Config.LOG_DIR, 'root_logger_default.log')),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.werkzeug': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': os.path.abspath(os.path.join(Config.LOG_DIR, 'werkzeug.log')),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
        'file.handler.data_view': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'data_view',
            'filename': os.path.abspath(os.path.join(Config.LOG_DIR, 'data_view.log')),
            'maxBytes': 10000000,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default', 'file.handler.default_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['default', 'file.handler.default_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'information': {
            'handlers': ['file.handler.information'],
            'level': 'INFO',
            'propagate': False
        },
        'werkzeug': {  # if __name__ == '__main__'
            'handlers': ['file.handler.werkzeug'],
            'level': 'DEBUG',
            'propagate': False
        },
        'data_view': {  # if __name__ == '__main__'
            'handlers': ['file.handler.data_view'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}

