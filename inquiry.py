"""
inquiry.py
----------
Defines the Inquiry class - represents a customer enquiry against a property.
Maps to the Inquiry class in the SDS UML Class Diagram (Fig. 1) and
supports SRS requirement RE-9 (contact CSS for viewings/inquiries).
"""

import datetime
from log_singleton import Log


class Inquiry:
    """A customer inquiry sent to a Customer Service Supervisor."""

    VALID_STATUSES = ("Pending", "Responded", "Closed")

    def __init__(self, inquiry_id: int, user_id: int, property_id: int,
                 message: str, preferred_date: datetime.date = None):
        if not message or len(message.strip()) == 0:
            raise ValueError("Inquiry message cannot be empty.")

        self.inquiry_id = inquiry_id
        self.user_id = user_id
        self.property_id = property_id
        self.message = message
        self.preferred_date = preferred_date
        self.status = "Pending"
        self.date_submitted = datetime.datetime.now()

    def submit(self) -> None:
        """Submit this inquiry into the system and log the action."""
        Log().create_log("InquirySubmitted",
                         f"Inquiry {self.inquiry_id} submitted by user "
                         f"{self.user_id} on property {self.property_id}.")

    def update_status(self, new_status: str) -> None:
        """Update the inquiry status with validation."""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {new_status}. Must be one of "
                             f"{self.VALID_STATUSES}.")
        self.status = new_status
        Log().create_log("InquiryUpdated",
                         f"Inquiry {self.inquiry_id} status -> {new_status}.")

    def notify_css(self) -> None:
        """Notify a Customer Service Supervisor about this inquiry."""
        Log().create_log("CSSNotified",
                         f"CSS notified about inquiry {self.inquiry_id}.")
