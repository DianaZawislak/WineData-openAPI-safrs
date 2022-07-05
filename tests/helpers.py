"""These are functions that help with testing"""
import json
import logging

from app.logging_config import logging_setup


def print_json_to_data_view_log_nicely(data):
    """This will print to ../logs/data_view.log"""
    logging_setup()
    data_view_logger = logging.getLogger("data_view")
    data_view_logger.info(json.dumps(data, indent=2))
