# -*- coding: utf-8 -*-
"""
Module for storing basic data structures of mock data for testing.
"""
mock_customer_data = {
    "id": "1b2f7b83-7b4d-441d-a210-afaa970e5b76",
    "data": {
        "SUBSCRIPTION": "basic",
        "CREATION_DATE": "2013-03-10T02:00:00Z",
        "LAST_PAYMENT_DATE": "2020-01-10T09:25:00Z",
        "theme_name": "Tropical Island",
        "ENABLED_FEATURES": {
            "CERTIFICATES_INSTRUCTOR_GENERATION": True,
            "INSTRUCTOR_BACKGROUND_TASKS": True,
            "ENABLE_COURSEWARE_SEARCH": True,
            "ENABLE_COURSE_DISCOVERY": True,
            "ENABLE_DASHBOARD_SEARCH": True,
            "ENABLE_EDXNOTES": True,
        },
        "language_code": "en",
        "banner_message": "<p><span>Welcome</span> to Mr X's website</p>",
        "displayed_timezone": "America/Bogota",
        "user_profile_image": "https://i.imgur.com/LMhM8nn.jpg",
        "user_email": "barack@aol.com",
    },
}

mock_manager_arguments = {
    "new_subscription": "basic",
    "customer_id": "9f5c5a5f-4f4c-4a4c-a5f5-5c5f9f4f4c4a",
    "customer_data_api_url": "http://localhost:8010/api/v1/customerdata/",
    "subscriptions": {"free": 1, "basic": 2, "premium": 3},
}

subscription_levels = {
    "low_subscription": 1,
    "mid_subscription": 2,
    "high_subscription": 3,
}

subscription_manager_attributes = [
    "customer_id",
    "new_subscription",
    "customer_data_api_url",
    "subscriptions",
    "customer_data",
    "old_subscription",
    "changes_sent",
]
