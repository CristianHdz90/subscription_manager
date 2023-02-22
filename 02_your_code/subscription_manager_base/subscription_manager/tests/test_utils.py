"""
Test the core classes of the subscription manager library.
"""
from unittest import TestCase
from datetime import datetime
from subscription_manager_base.subscription_manager.utils import get_standard_datetime


class TestUtils(TestCase):
    """
    Tests for the utility functions.
    """

    def test_get_standard_datetime_returns_well_formatted_datetime_string(self):
        """
        Tests if the get_standard_datetime method returns a
        datetime string with the expected format.
        """
        datetime_string = get_standard_datetime()
        try:
            datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            self.fail("Incorrect date format")
