"""
Testing the django rest framework configuration
"""

from django.test import TestCase
from rest_framework.test import APIClient


class CustomerDataAPITestCase(TestCase):
    """
    Basic test case that asserts that we can actually call the API
    """

    def test_can_reach_api(self):
        """
        Asserts that calling the API actually works
        """
        client = APIClient()
        response = client.get("/api/v1/customerdata/")

        self.assertEqual(response.status_code, 200)
