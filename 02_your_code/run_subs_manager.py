# -*- coding: utf-8 -*-
"""
Simple Python for connecting the CLI to the subscription manager library.

Examples of usage:
python run_subs_manager.py upgrade 1b2f7b83-7b4d-441d-a210-afaa970e5b76 premium
    output: 1b2f7b83-7b4d-441d-a210-afaa970e5b76 -- UPGRADED -- from free to premium

python run_subs_manager.py downgrade 1b2f7b83-7b4d-441d-a210-afaa970e5b76 free
    output: 1b2f7b83-7b4d-441d-a210-afaa970e5b76 -- DOWNGRADED -- from premium to free

Note: This file is only for testing purposes of the subscription manager library,
and is not designed for being used in a production environment. 
"""

import sys

from subscription_manager_base.subscription_manager.core import (
    DowngradeSubscription,
    UpgradeSubscription,
)

if __name__ == "__main__":
    customer_data_api_url = "http://localhost:8010/api/v1/customerdata/"
    subscriptions = {
        "free": 1,
        "basic": 2,
        "premium": 3,
    }

    if len(sys.argv) < 4:
        print("Usage: python script.py upgrade/downgrade uuid plan")
    else:
        command = sys.argv[1]
        uuid = sys.argv[2]
        new_subscription = sys.argv[3]

        if command == "upgrade":
            upgrade_manager = UpgradeSubscription(
                uuid, new_subscription, customer_data_api_url, subscriptions
            )
            print(upgrade_manager.upgrade())
        if command == "downgrade":
            downgrade_manager = DowngradeSubscription(
                uuid, new_subscription, customer_data_api_url, subscriptions
            )
            print(downgrade_manager.downgrade())
