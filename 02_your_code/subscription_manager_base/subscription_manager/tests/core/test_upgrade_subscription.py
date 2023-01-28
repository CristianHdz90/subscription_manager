# -*- coding: utf-8 -*-
"""
Test the UpgradeSubscription class from the core.py file.
"""
from unittest import TestCase, mock

from subscription_manager_base.subscription_manager.core import UpgradeSubscription
from subscription_manager_base.subscription_manager.tests.mocks.mock_data import (
    mock_customer_data,
    mock_manager_arguments,
    subscription_levels,
)
from subscription_manager_base.subscription_manager.tests.mocks.mock_objects import (
    MockResponse,
)


class TestUpgradeSubscription(TestCase):
    """
    Tests for the upgrade subscription class.
    """

    def setUp(self):
        """
        Setup common conditions for test cases.
        """
        self.testing_customer_data = mock_customer_data
        upgrade_manager = UpgradeSubscription(**mock_manager_arguments)
        self.upgrade_subscription_manager = upgrade_manager

        mock_response = MockResponse(
            status_code=200, response_data=self.testing_customer_data
        )
        self.mock_response = mock.MagicMock(return_value=mock_response)

    def test_upgrade_is_valid_returns_true(self):
        """
        Tests if the upgrade_is_valid method returns
        True when an upgrade is valid.
        """
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.subscriptions = subscription_levels

        upgrade_manager.old_subscription = "low_subscription"
        upgrade_manager.new_subscription = "high_subscription"

        self.assertTrue(upgrade_manager.upgrade_is_valid())

    def test_upgrade_is_valid_returns_false(self):
        """
        Tests if the upgrade_is_valid method returns
        False when an upgrade is not valid.
        """
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.subscriptions = subscription_levels

        upgrade_manager.old_subscription = "high_subscription"
        upgrade_manager.new_subscription = "low_subscription"

        self.assertFalse(upgrade_manager.upgrade_is_valid())

    def test_upgrade_is_valid_logs_an_error(self):
        """
        Tests if the upgrade_is_valid method logs an
        error when an upgrade is not valid.
        """
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.subscriptions = subscription_levels

        upgrade_manager.old_subscription = "high_subscription"
        upgrade_manager.new_subscription = "low_subscription"

        with self.assertLogs() as logs_captured:
            upgrade_manager.upgrade_is_valid()

        expected_message = (
            f"Attempted to upgrade from {upgrade_manager.old_subscription} "
            f"to {upgrade_manager.new_subscription}."
        )
        self.assertEqual(len(logs_captured.records), 1)
        self.assertEqual(logs_captured.records[0].message, expected_message)

    def test_upgrade_method_gets_the_customer_data(self):
        """
        Tests if the customer data is gotten when the
        upgrade method is called.
        """
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.new_subscription = "premium"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            upgrade_manager.upgrade()

            self.assertTrue(hasattr(upgrade_manager, "customer_data"))
            self.assertIn("id", upgrade_manager.customer_data)
            self.assertIn("data", upgrade_manager.customer_data)

    def test_upgrade_method_removes_downgrade_date_keyword_from_customer_data(self):
        """
        Tests if the DOWNGRADE_DATE keyword is removed from the
        customer data when the upgrade method is called.
        """
        self.testing_customer_data["DOWNGRADE_DATE"] = ""
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.new_subscription = "premium"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            upgrade_manager.upgrade()

            self.assertNotIn("DOWNGRADE_DATE", upgrade_manager.customer_data["data"])

    def test_upgrade_method_adds_upgrade_date_keyword_to_customer_data(self):
        """
        Tests if the UPGRADE_DATE keyword is added to the
        customer data when the upgrade method is called.
        """
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.new_subscription = "premium"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            upgrade_manager.upgrade()

            self.assertIn("UPGRADE_DATE", upgrade_manager.customer_data["data"])

    def test_upgrade_method_changes_subscription_in_customer_data(self):
        """
        Tests if the new subscription is installed in the customer
        data the when the upgrade method is called.
        """
        self.testing_customer_data["data"]["SUBSCRIPTION"] = "free"
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.new_subscription = "premium"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            upgrade_manager.upgrade()

            subscription = upgrade_manager.customer_data["data"]["SUBSCRIPTION"]
            self.assertEqual(subscription, "premium")

    def test_upgrade_method_returns_report_of_changes(self):
        """
        Tests if the upgrade method returns a string with
        the report of changes when the upgrade succeeds.
        """
        upgrade_manager = self.upgrade_subscription_manager
        upgrade_manager.new_subscription = "premium"

        kwargs = {"get": self.mock_response, "put": self.mock_response}
        with mock.patch.multiple("requests", **kwargs):
            report = upgrade_manager.upgrade()

        expected_message = (
            f"{upgrade_manager.customer_id} -- UPGRADED -- "
            f"from {upgrade_manager.old_subscription} "
            f"to {upgrade_manager.new_subscription}"
        )
        self.assertEqual(report, expected_message)

    def test_upgrade_method_returns_error_string(self):
        """
        Tests if the upgrade method returns an error
        string when the upgrade fails.
        """
        upgrade_manager = self.upgrade_subscription_manager
        returned_message = upgrade_manager.upgrade()

        expected_message = "Failed to upgrade."
        self.assertEqual(returned_message, expected_message)
