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

    def __init__(self, status_code, response_data=None):
        """
        Initialize a new instance of the class with the given
        status code and response data.

        Attributes:
        - status_code (int): The HTTP status code of the mock response.
        - response_data (dict): Data to be returned in the response body.
        """
        self.status_code = status_code
        self._response_data = response_data or {}

    @property
    def text(self):
        """
        Simulates the 'text' attribute of a real response.
        """
        return json.dumps(self._response_data)
