# -*- coding: utf-8 -*-
"""
Module for storing mock objects for testing.
"""
import json


class MockResponse:  # pylint: disable=R0903
    """
    This class provides a mock response object
    that can be used for testing purposes.
    """

    def __init__(self, status_code, reason="", response_data=None):
        """
        Initialize a new instance of the class with the given
        status code and response data.

        Attributes:
        - status_code (int):    The HTTP status code of the mock response.
        - reason (str):         Short description of the HTTP response.
        - response_data (dict): Data to be returned in the response body.
        """
        self.status_code = status_code
        self.reason = reason
        self._response_data = response_data or {}

    @property
    def text(self):
        """
        Simulates the 'text' attribute of a real response.
        """
        return json.dumps(self._response_data)
