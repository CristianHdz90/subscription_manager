# -*- coding: utf-8 -*-
"""
Core classes of the subscription manager library.
"""
import json

import requests
from subscription_manager_base.subscription_manager.logging_config import logging
from subscription_manager_base.subscription_manager.utils import get_standard_datetime


class SubscriptionManager:
    """
    The SubscriptionManager class is used for managing customer subscriptions.
    Is the base class for UpgradeSubscription and DowngradeSubscription.
    """

    def __init__(
        self, customer_id, new_subscription, customer_data_api_url, subscriptions
    ):
        """
        Attributes:
        - customer_id (int): The ID of the customer.
        - new_subscription (str): The new subscription plan for the customer.
        - customer_data_api_url (str): The URL of the API used to retrieve customer data.
        - subscriptions (dict): Dictionary with the available subscription plans and their levels.
        - customer_data (dict): Dictionary to store the customer data.
        - changes_sent (bool): Check to confirm when the changes were correctly sent to the API.
        - old_subscription (str): The old subscription of the customer to be replaced.
        """
        self.customer_id = customer_id
        self.new_subscription = new_subscription
        self.customer_data_api_url = customer_data_api_url
        self.subscriptions = subscriptions
        self.customer_data = {}
        self.old_subscription = ""
        self.changes_sent = False

    def get_url(self):
        """
        Returns the full URL to the configuration
        data of given customer id.
        """
        return f"{self.customer_data_api_url}{self.customer_id}/"

    def get_customer_data(self):
        """
        Retrieves customer data obtained from the
        customer data API.
        """
        url = self.get_url()

        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                self.customer_data = json.loads(response.text)
                self.old_subscription = self.customer_data["data"]["SUBSCRIPTION"]
            else:
                message = (
                    f"Failed to retrieve the customer data "
                    f"[{response.status_code} {response.reason}]."
                )
                logging.error(message)
        except requests.exceptions.RequestException:
            message = (
                "The customer data API is currently "
                "unavailable, please try again later."
            )
            logging.error(message)

    def delete_item(self, key):
        """
        Deletes a specific item from the customer data.
        """
        if key in self.customer_data["data"]:
            del self.customer_data["data"][key]

    def add_or_update_item(self, key, value):
        """
        Adds or updates a specific item from the customer data.
        """
        self.customer_data["data"][key] = value

    def send_changes_to_customer_data_api(self):
        """
        Sends the final changes to the customer data API.
        """
        url = self.get_url()
        try:
            response = requests.put(url, json=self.customer_data, timeout=5)
            if response.status_code == 200:
                self.changes_sent = True
            else:
                message = (
                    f"Failed to update the customer data "
                    f"[{response.status_code} {response.reason}]."
                )
                logging.error(message)
        except requests.exceptions.RequestException:
            message = (
                "The customer data API is currently "
                "unavailable, please try again later."
            )
            logging.error(message)

    def subscription_is_valid(self):
        """
        Checks if the new subscription level provided is
        in the dictionary of available subscriptions.
        """
        if self.new_subscription in self.subscriptions:
            return True
        message = (
            "The new subscription level provided is not "
            "in the available subscriptions."
        )
        logging.error(message)
        return False

    def report_of_changes(self, action):
        """
        Return a basic report of the changes done to the
        customer data.
        """
        old = self.old_subscription
        new = self.new_subscription
        return f"{self.customer_id} -- {action} -- from {old} to {new}"

    def new_subscription_level_is_free(self):
        """
        Checks if the new provided subscription
        level is the 'free' subscription.
        """
        return "free" in self.new_subscription.lower()

    def disable_features(self):
        """
        This disables all the enabled features.
        """
        features = self.customer_data["data"]["ENABLED_FEATURES"]
        for feature in features.keys():
            features[feature] = False


class UpgradeSubscription(SubscriptionManager):
    """
    The main class for upgrading the subscription level
    in the configuration data of a specific customer.
    """

    def upgrade_is_valid(self):
        """
        Validation to check if the new subscription
        level is greater than the old one.
        """
        new_subscription_level = self.subscriptions[self.new_subscription]
        old_subscription_level = self.subscriptions[self.old_subscription]

        if new_subscription_level > old_subscription_level:
            return True

        message = (
            f"Attempted to upgrade from {self.old_subscription} "
            f"to {self.new_subscription}."
        )
        logging.error(message)
        return False

    def upgrade(self):
        """
        Upgrades the subscription level in the condiguration
        data of a specific customer.
        """
        self.get_customer_data()
        if self.customer_data:
            if self.subscription_is_valid() and self.upgrade_is_valid():
                self.delete_item("DOWNGRADE_DATE")
                self.add_or_update_item("UPGRADE_DATE", get_standard_datetime())
                self.add_or_update_item("SUBSCRIPTION", self.new_subscription)

                self.send_changes_to_customer_data_api()
                if self.changes_sent:
                    return self.report_of_changes("UPGRADED")
        return "Failed to upgrade."


class DowngradeSubscription(SubscriptionManager):
    """
    The main class for downgrading the subscription level
    in the configuration data of a specific customer.
    """

    def downgrade_is_valid(self):
        """
        Validation to check if the new subscription
        level is lower than the old one.
        """
        new_subscription_level = self.subscriptions[self.new_subscription]
        old_subscription_level = self.subscriptions[self.old_subscription]

        if new_subscription_level < old_subscription_level:
            return True

        message = (
            f"Attempted to downgrade from {self.old_subscription} "
            f"to {self.new_subscription}."
        )
        logging.error(message)
        return False

    def downgrade(self):
        """
        Downgrades the subscription level in the condiguration
        data of a specific customer.
        """
        self.get_customer_data()
        if self.customer_data:
            if self.subscription_is_valid() and self.downgrade_is_valid():

                self.delete_item("UPGRADE_DATE")
                if self.new_subscription_level_is_free():
                    self.disable_features()
                self.add_or_update_item("DOWNGRADE_DATE", get_standard_datetime())
                self.add_or_update_item("SUBSCRIPTION", self.new_subscription)

                self.send_changes_to_customer_data_api()
                if self.changes_sent:
                    return self.report_of_changes("DOWNGRADED")
        return "Failed to downgrade."
