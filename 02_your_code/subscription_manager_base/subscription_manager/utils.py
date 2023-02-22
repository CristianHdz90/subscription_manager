# -*- coding: utf-8 -*-
"""
Utilities for the subscription manager library.
"""
from datetime import datetime

import pytz


def get_standard_datetime():
    """
    This function returns a datetime in string
    format that follows the iso 8601 standard.
    """
    now = datetime.now(pytz.utc)
    iso_8601_datetime_standard = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    return iso_8601_datetime_standard
