"""
notification.py
---------------
Defines the Notification class which implements the Observer pattern alongside
Property (the Subject) and Customer (the Observer). Maps to the Observer
Pattern diagram in the SDS (Fig. 4) and supports SRS requirement RE-10
(subscribe to similar properties) and RE-8 (automated emails).
"""

import datetime
from log_singleton import Log


class Notification:
    """Notification message sent to a Customer when an event occurs."""

    VALID_TYPES = ("PropertyAlert", "ViewingConfirmation", "Inquiry")

    def __init__(self, notification_id: int, user_id: int,
                 notification_type: str, message: str):
        if notification_type not in self.VALID_TYPES:
            raise ValueError(f"Invalid notification type: {notification_type}.")

        self.notification_id = notification_id
        self.user_id = user_id
        self.notification_type = notification_type
        self.message = message
        self.status = "Pending"
        self.date_sent = datetime.datetime.now()

    def send_notification(self) -> None:
        """Send this notification via the External Email Service (AC-5)."""
        # In production this would hand off to the External Email Service.
        # For the prototype we simulate the delivery and mark it sent.
        self.status = "Sent"
        Log().create_log("Notification",
                         f"Notification {self.notification_id} sent to "
                         f"user {self.user_id}.")

    def send_property_alert(self) -> None:
        """Trigger a property alert notification (Observer pattern)."""
        self.notification_type = "PropertyAlert"
        self.send_notification()

    def send_viewing_confirmation(self) -> None:
        """Trigger a viewing confirmation notification."""
        self.notification_type = "ViewingConfirmation"
        self.send_notification()
