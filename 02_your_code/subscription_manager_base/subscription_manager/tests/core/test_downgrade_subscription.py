# -*- coding: utf-8 -*-
"""
Test the DowngradeSubscription class from the core.py file.
"""
from unittest import TestCase, mock

from subscription_manager_base.subscription_manager.core import DowngradeSubscription
from subscription_manager_base.subscription_manager.tests.mocks.mock_data import (
    mock_customer_data,
    mock_manager_arguments,
    subscription_levels,
)
from subscription_manager_base.subscription_manager.tests.mocks.mock_objects import (
    MockResponse,
)


class DowngradeSubscriptionTestCase(TestCase):
    """
    Tests for the downgrade subscription class.
    """

    def setUp(self):
        """
        Setup common conditions for test cases.
        """
        self.testing_customer_data = mock_customer_data
        downgrade_manager = DowngradeSubscription(**mock_manager_arguments)
        self.downgrade_subscription_manager = downgrade_manager

        mock_response = MockResponse(
            status_code=200, response_data=self.testing_customer_data
        )
        self.mock_response = mock.MagicMock(return_value=mock_response)

    def test_downgrade_is_valid_returns_true(self):
        """
        Tests if the downgrade_is_valid method returns
        True when a downgrade is valid.
        """
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.subscriptions = subscription_levels

        downgrade_manager.old_subscription = "high_subscription"
        downgrade_manager.new_subscription = "low_subscription"

        self.assertTrue(downgrade_manager.downgrade_is_valid())

    def test_downgrade_is_valid_returns_false(self):
        """
        Tests if the downgrade_is_valid method returns
        false when a downgrade is not valid.
        """
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.subscriptions = subscription_levels

        downgrade_manager.old_subscription = "low_subscription"
        downgrade_manager.new_subscription = "high_subscription"

        self.assertFalse(downgrade_manager.downgrade_is_valid())

    def test_downgrade_is_valid_changes_exit_code_attribute_to_5(self):
        """
        Tests if the downgrade_is_valid method changes the exit_code
        attribute to 5 when a downgrade is not valid.
        """
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.subscriptions = subscription_levels

        downgrade_manager.old_subscription = "low_subscription"
        downgrade_manager.new_subscription = "high_subscription"
        downgrade_manager.exit_code = 0

        downgrade_manager.downgrade_is_valid()

        self.assertEqual(downgrade_manager.exit_code, 5)

    def test_downgrade_is_valid_logs_an_error(self):
        """
        Tests if the downgrade_is_valid method logs an
        error when a downgrade is not valid.
        """
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.subscriptions = subscription_levels

        downgrade_manager.old_subscription = "low_subscription"
        downgrade_manager.new_subscription = "high_subscription"

        with self.assertLogs() as logs_captured:
            downgrade_manager.downgrade_is_valid()

        expected_message = (
            f"Attempted to downgrade from {downgrade_manager.old_subscription} "
            f"to {downgrade_manager.new_subscription}."
        )
        self.assertEqual(len(logs_captured.records), 1)
        self.assertEqual(logs_captured.records[0].message, expected_message)

    def test_downgrade_method_gets_the_customer_data(self):
        """
        Tests if the customer data is gotten when the
        downgrade method is called.
        """
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.new_subscription = "free"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            downgrade_manager.downgrade()

        self.assertTrue(hasattr(downgrade_manager, "customer_data"))
        self.assertIn("id", downgrade_manager.customer_data)
        self.assertIn("data", downgrade_manager.customer_data)

    def test_downgrade_method_removes_upgrade_date_keyword_from_customer_data(self):
        """
        Tests if the UPGRADE_DATE keyword is removed from the
        customer data when the downgrade method is called.
        """
        self.testing_customer_data["UPGRADE_DATE"] = ""
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.new_subscription = "free"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            downgrade_manager.downgrade()

        self.assertNotIn("UPGRADE_DATE", downgrade_manager.customer_data["data"])

    def test_downgrade_method_adds_downgrade_date_keyword_to_customer_data(self):
        """
        Tests if the DOWNGRADE_DATE keyword is added to the
        customer data when the downgrade method is called.
        """
        self.testing_customer_data["data"]["SUBSCRIPTION"] = "premium"
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.new_subscription = "free"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            downgrade_manager.downgrade()

        self.assertIn("DOWNGRADE_DATE", downgrade_manager.customer_data["data"])

    def test_downgrade_method_changes_subscription_in_customer_data(self):
        """
        Tests if the new subscription is installed in the customer
        data the when the downgrade method is called.
        """
        self.testing_customer_data["data"]["SUBSCRIPTION"] = "premium"
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.new_subscription = "free"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            downgrade_manager.downgrade()

        subscription = downgrade_manager.customer_data["data"]["SUBSCRIPTION"]
        self.assertEqual(subscription, "free")

    def test_downgrade_method_returns_report_of_changes(self):
        """
        Tests if the downgrade method returns a string with
        the report of changes when the downgrade succeeds.
        """
        downgrade_manager = self.downgrade_subscription_manager
        downgrade_manager.new_subscription = "free"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            report = downgrade_manager.downgrade()

        expected_message = (
            f"{downgrade_manager.customer_id} -- DOWNGRADED -- "
            f"from {downgrade_manager.old_subscription} "
            f"to {downgrade_manager.new_subscription}"
        )
        self.assertEqual(report, expected_message)

    def test_downgrade_method_calls_system_exit_when_downgrade_fails(self):
        """
        Tests if the downgrade method calls the 'sys.exit()'
        method when the downgrade fails.
        """
        downgrade_manager = self.downgrade_subscription_manager
        with self.assertRaises(SystemExit) as c_manager:
            downgrade_manager.downgrade()

        self.assertTrue(c_manager.exception.code != 0)
