# -*- coding: utf-8 -*-
"""
Additional configurations for the logging module.
"""
import logging

logging.basicConfig(filename="error.log", format="%(message)s", filemode="w")
