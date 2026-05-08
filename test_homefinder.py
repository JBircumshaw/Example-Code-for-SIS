"""
test_homefinder.py
------------------
Unit tests and integration tests for HomeFinder.

Covers two prioritised SRS requirements:
  - RE-15/RE-16 (Secure logging via Singleton pattern)
  - RE-6      (Search/filter properties)

Plus two integration tests covering end-to-end flows.

Run with:
    python -m unittest test_homefinder.py -v
"""

import unittest
import datetime

from log_singleton import Log
from user import Customer, Administrator
from property import Property
from inquiry import Inquiry
from payment import Payment
from notification import Notification


class TestLogSingleton(unittest.TestCase):
    """TC-01 - Verifies the Singleton pattern behaviour for the Log class.
    Maps to SRS requirements RE-15 (transaction logging) and RE-16
    (search/inquiry logging)."""

    def setUp(self):
        Log().clear()

    def test_only_one_instance_exists(self):
        """Two calls to Log() must return the same object."""
        log1 = Log()
        log2 = Log()
        self.assertIs(log1, log2,
                      "Log() returned two different instances - Singleton broken.")

    def test_shared_log_entries(self):
        """An entry written through one reference must be visible through another."""
        log1 = Log()
        log2 = Log()
        log1.create_log("Payment", "Test payment entry")
        self.assertEqual(len(log2.view_logs()), 1,
                         "Log entries are not shared between Singleton references.")
        self.assertEqual(log2.view_logs()[0]["action_type"], "Payment")


class TestPropertySearch(unittest.TestCase):
    """TC-02 - Verifies search_properties() correctly filters by location
    and max price. Maps to SRS requirement RE-6 (search filters)."""

    def setUp(self):
        Log().clear()
        self.customer = Customer(user_id=10, email="test@example.com",
                                 password="secure123")
        self.properties = [
            Property(1, "Derby", 200000, "Residential", 3, "Garden"),
            Property(2, "Derby", 350000, "Residential", 4, "Garden, Garage"),
            Property(3, "Nottingham", 180000, "Residential", 2, "None")
        ]

    def test_filter_by_location_and_price(self):
        """Search should return only properties matching all supplied filters."""
        results = self.customer.search_properties(
            self.properties, location="Derby", max_price=250000)
        self.assertEqual(len(results), 1,
                         "Expected exactly 1 Derby property under £250k.")
        self.assertEqual(results[0].property_id, 1)

    def test_search_returns_empty_when_no_match(self):
        """A search with no matching listings should return an empty list."""
        results = self.customer.search_properties(
            self.properties, location="London")
        self.assertEqual(results, [])

    def test_invalid_input_raises(self):
        """Passing a non-list to search_properties must raise TypeError."""
        with self.assertRaises(TypeError):
            self.customer.search_properties("not a list", location="Derby")


class TestInquiryAndNotificationIntegration(unittest.TestCase):
    """IT-01 - Integration test covering the inquiry / notification flow.
    Validates that submitting an inquiry produces the correct chain of log
    entries spanning multiple classes (Customer, Inquiry, Notification, Log).
    Maps to UC-5 in the SDS and SRS requirements RE-8, RE-9."""

    def setUp(self):
        Log().clear()

    def test_inquiry_submission_triggers_logs_and_notification(self):
        customer = Customer(20, "buyer@example.com", "buyerpass")
        inquiry = Inquiry(inquiry_id=900, user_id=customer.user_id,
                          property_id=55,
                          message="Is this property still available?")
        customer.submit_inquiry(inquiry)

        notif = Notification(notification_id=300, user_id=customer.user_id,
                             notification_type="Inquiry",
                             message="Inquiry received.")
        notif.send_notification()

        log_entries = Log().view_logs()
        action_types = [entry["action_type"] for entry in log_entries]

        # We expect at least one Inquiry log and one Notification log
        self.assertIn("InquirySubmitted", action_types)
        self.assertIn("Notification", action_types)


class TestPaymentAndLoggingIntegration(unittest.TestCase):
    """IT-02 - Integration test covering payment flow + logging.
    Validates that a successful payment writes the correct transaction record
    to the Singleton Log, satisfying RE-14 (secure payment) and
    RE-15 (transaction logging)."""

    def setUp(self):
        Log().clear()

    def test_payment_success_logs_transaction(self):
        customer = Customer(30, "payer@example.com", "payerpass")
        payment = Payment(payment_id=800, user_id=customer.user_id,
                          amount=50.00, payment_method="CreditCard")

        success = customer.make_payment(payment)
        self.assertTrue(success)
        self.assertTrue(payment.confirm_payment())

        # The payment log entry must exist in the Singleton log
        log_entries = Log().view_logs()
        payment_logs = [e for e in log_entries if e["action_type"] == "Payment"]
        self.assertEqual(len(payment_logs), 1,
                         "Expected exactly one Payment log entry.")
        self.assertIn("£50.0", payment_logs[0]["details"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
