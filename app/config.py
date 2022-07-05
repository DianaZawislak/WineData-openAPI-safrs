import os


class Config(object):
    """This provides configuration information"""
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
    LOG_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'logs'))
