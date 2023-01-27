# -*- coding: utf-8 -*-
"""
Test the SubscriptionManager class from the core.py file.
"""
from unittest import TestCase, mock

from subscription_manager_base.subscription_manager.core import SubscriptionManager
from subscription_manager_base.subscription_manager.tests.mocks.mock_data import (
    mock_customer_data,
    mock_manager_arguments,
)
from subscription_manager_base.subscription_manager.tests.mocks.mock_objects import (
    MockResponse,
)


class TestSubscriptionManager(TestCase):
    """
    Tests for the subscription manager class.
    """

    def setUp(self):
        """
        Setup common conditions for test cases.
        """
        self.testing_customer_data = mock_customer_data
        subscription_manager = SubscriptionManager(**mock_manager_arguments)
        self.testing_subscription_manager = subscription_manager

    def test_constructor_takes_the_customer_id_argument(self):
        """
        Tests if the constructor of the subscription manager
        takes a customer_id argument.
        """
        customer_id = "7d1b9f63-9c2e-4f6f-9a5c-d5e3c3f8a7e5"
        args = [customer_id, "", "", {}]
        manager = SubscriptionManager(*args)
        self.assertEqual(manager.customer_id, customer_id)

    def test_constructor_takes_the_new_subscription_argument(self):
        """
        Tests if the constructor of the subscription manager
        takes a new_subscription argument.
        """
        manager = SubscriptionManager("", "free", "", {})
        self.assertEqual(manager.new_subscription, "free")

    def test_constructor_takes_the_customer_data_api_url_argument(self):
        """
        Tests if the constructor of the subscription manager
        takes a customer_data_api_url argument.
        """
        api_url = "http://localhost:8010/api/v1/customerdata/"
        args = ["", "", api_url, {}]
        manager = SubscriptionManager(*args)
        self.assertEqual(manager.customer_data_api_url, api_url)

    def test_constructor_takes_the_subscriptions_argument(self):
        """
        Tests if the constructor of the subscription manager
        takes a subscriptions argument.
        """
        subscriptions = {"free": 1, "basic": 2, "premium": 3}
        manager = SubscriptionManager("", "", "", subscriptions)
        self.assertEqual(manager.subscriptions, subscriptions)

    def test_get_url_returns_correct_url_given_customer_id(self):
        """
        Tests if the get_utl method returns the full URL
        to a specific customer data.
        """
        url = (
            "http://localhost:8010/api/v1/customerdata/"
            + "9f5c5a5f-4f4c-4a4c-a5f5-5c5f9f4f4c4a/"
        )
        self.assertEqual(url, self.testing_subscription_manager.get_url())

    def test_get_customer_data_saves_customer_data_in_customer_data_attribute(self):
        """
        Tests if the get_customer_data method gets the customer data
        and saves it in the customer_data attribute.
        """
        mock_response = MockResponse(
            status_code=200, response_data=self.testing_customer_data
        )
        use_mock_response = mock.patch("requests.get", return_value=mock_response)
        with use_mock_response:
            manager = self.testing_subscription_manager
            manager.get_customer_data()

            self.assertTrue(hasattr(manager, "customer_data"))
            self.assertEqual(manager.customer_data, self.testing_customer_data)

    def test_get_customer_data_raises_error_when_cannot_get_customer_data(self):
        """
        Tests if the get_customer_data method raises and error when
        it could not get the customer data from the customer data API.
        """
        mock_response = MockResponse(status_code=404)
        use_mock_response = mock.patch("requests.get", return_value=mock_response)

        with use_mock_response:
            manager = self.testing_subscription_manager
            self.assertRaises(ValueError, manager.get_customer_data)

    def test_get_customer_data_saves_old_subscription_in_the_subscription_manager(self):
        """
        Tests if the get_customer_data method saves the old subscription
        in an old_subscription attribute after getting the customer data.
        """
        manager = self.testing_subscription_manager
        manager.customer_data = self.testing_customer_data
        mock_response = MockResponse(
            status_code=200, response_data=self.testing_customer_data
        )
        use_mock_response = mock.patch("requests.get", return_value=mock_response)
        with use_mock_response:
            manager.get_customer_data()

        self.assertTrue(hasattr(manager, "old_subscription"))
        self.assertEqual(manager.old_subscription, "basic")

    def test_delete_item_deletes_specific_item_from_customer_data(self):
        """
        Tests if the delete_item method deletes a specific
        item from the customer data given its key.
        """
        manager = self.testing_subscription_manager
        manager.customer_data = self.testing_customer_data

        manager.customer_data["data"]["DATA_TO_DELETE"] = "data to delete"
        manager.delete_item("DATA_TO_DELETE")

        self.assertNotIn("DATA_TO_DELETE", manager.customer_data["data"])

    def test_add_or_update_item_adds_item_to_customer_data(self):
        """
        Tests if the add_or_update_item method adds a given
        item to the customer data.
        """
        manager = self.testing_subscription_manager
        manager.customer_data = self.testing_customer_data

        manager.add_or_update_item("ITEM_TO_ADD", "value")

        self.assertIn("ITEM_TO_ADD", manager.customer_data["data"])
        self.assertEqual(manager.customer_data["data"]["ITEM_TO_ADD"], "value")

    def test_add_or_update_item_updates_item_to_customer_data(self):
        """
        Tests if the add_or_update_item method updates a given
        item in the customer data.
        """
        manager = self.testing_subscription_manager
        manager.customer_data = self.testing_customer_data

        manager.add_or_update_item("SUBSCRIPTION", "basic")

        self.assertIn("SUBSCRIPTION", manager.customer_data["data"])
        self.assertEqual(manager.customer_data["data"]["SUBSCRIPTION"], "basic")

    def test_send_changes_to_customer_data_api_raises_error(self):
        """
        Tests if the send_changes_to_customer_data_api method raises an
        error when the API did not take the customer data successfully.
        """
        manager = self.testing_subscription_manager
        manager.customer_data = self.testing_customer_data
        mock_response = MockResponse(status_code=400)

        use_mock_response = mock.patch("requests.put", return_value=mock_response)
        with use_mock_response:
            send_changes = manager.send_changes_to_customer_data_api
            self.assertRaises(ValueError, send_changes)

    def test_subscription_is_valid_returns_true(self):
        """
        Tests if the subscription_is_valid method returns
        True when the new subscription is in the group of
        available subscriptions.
        """
        manager = self.testing_subscription_manager
        manager.new_subscription = "basic"
        self.assertTrue(manager.subscription_is_valid())

    def test_subscription_is_valid_raises_error(self):
        """
        Tests if the subscription_is_valid method returns
        True when the new subscription is not in the group
        of available subscriptions.
        """
        manager = self.testing_subscription_manager
        manager.new_subscription = "fake_subscription"
        self.assertRaises(ValueError, manager.subscription_is_valid)

    def test_report_of_changes_returns_string(self):
        """
        Tests if the report_of_changes method returns a string.
        """
        manager = self.testing_subscription_manager
        manager.old_subscription = "free"
        manager.new_subscription = "premium"
        self.assertEqual(str, type(manager.report_of_changes("ACTION_DONE")))

    def test_new_subscription_level_is_free_returns_true(self):
        """
        Tests if the new_subscription_level_is_free method returns
        True when the new_subscription attribute is equal to 'free'.
        """
        manager = self.testing_subscription_manager
        manager.new_subscription = "free"
        self.assertTrue(manager.new_subscription_level_is_free())

    def test_new_subscription_level_is_free_returns_false(self):
        """
        Tests if the new_subscription_level_is_free method returns
        True when the new_subscription attribute is not equal to 'free'.
        """
        manager = self.testing_subscription_manager
        manager.new_subscription = "premium"
        self.assertFalse(manager.new_subscription_level_is_free())

    def test_disable_features_changes_all_enabled_features_in_customer_data_to_false(
        self,
    ):
        """
        Tests if the disable_features method changes all the enabled_features
        in the customer data to False.
        """
        manager = self.testing_subscription_manager
        manager.customer_data = self.testing_customer_data

        manager.disable_features()
        features = manager.customer_data["data"]["ENABLED_FEATURES"]
        for feat in features.values():
            self.assertFalse(feat)
