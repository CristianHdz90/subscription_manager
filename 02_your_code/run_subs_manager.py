# -*- coding: utf-8 -*-
"""
Simple Python script to connect the CLI to the subscription manager library.

Examples of usage:

python run_subs_manager.py upgrade 1b2f7b83-7b4d-441d-a210-afaa970e5b76 premium
    output: 1b2f7b83-7b4d-441d-a210-afaa970e5b76 -- UPGRADED -- from free to premium

python run_subs_manager.py downgrade 1b2f7b83-7b4d-441d-a210-afaa970e5b76 free
    output: 1b2f7b83-7b4d-441d-a210-afaa970e5b76 -- DOWNGRADED -- from premium to free
"""
import sys

from settings_subs_manager import CUSTOMER_DATA_API_URL, SUBSCRIPTIONS
from subscription_manager_base.subscription_manager.core import (
    DowngradeSubscription,
    UpgradeSubscription,
)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python script.py upgrade/downgrade uuid plan")
    else:
        COMMAND = sys.argv[1]
        UUID = sys.argv[2]
        NEW_SUBSCRIPTION = sys.argv[3]

        if COMMAND == "upgrade":
            upgrade_manager = UpgradeSubscription(
                UUID, NEW_SUBSCRIPTION, CUSTOMER_DATA_API_URL, SUBSCRIPTIONS
            )
            print(upgrade_manager.upgrade())
        if COMMAND == "downgrade":
            downgrade_manager = DowngradeSubscription(
                UUID, NEW_SUBSCRIPTION, CUSTOMER_DATA_API_URL, SUBSCRIPTIONS
            )
            print(downgrade_manager.downgrade())
