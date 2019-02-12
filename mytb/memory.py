from __future__ import absolute_import

"""
Helper to get info about memory consumption
"""

import logging
import os

import psutil


logger = logging.getLogger(__name__)


def get_rss():
    pid = psutil.Process(os.getpid())
    return pid.memory_info().rss


def log_rss():
    logger.debug("RSS: %d", get_rss())
