import unittest

from log_singleton import Log
from user import Customer
from property import Property
from inquiry import Inquiry
from payment import Payment
from notification import Notification


class TestLogSingleton(unittest.TestCase):
    # TC-01 - tests that the Singleton pattern works for the Log class

    def setUp(self):
        Log().clear()

    def test_only_one_instance(self):
        log1 = Log()
        log2 = Log()
        self.assertIs(log1, log2)

    def test_shared_log_entries(self):
        log1 = Log()
        log2 = Log()
        log1.create_log("Payment", "Test entry")
        self.assertEqual(len(log2.view_logs()), 1)


class TestPropertySearch(unittest.TestCase):
    # TC-02 - tests that the search filter returns only matching properties

    def setUp(self):
        Log().clear()
        self.customer = Customer(10, "test@example.com", "testpass")
        self.properties = [
            Property(1, "Derby", 200000, "Residential", 3, "Garden"),
            Property(2, "Derby", 350000, "Residential", 4, "Garden, Garage"),
            Property(3, "Nottingham", 180000, "Residential", 2, "None")
        ]

    def test_filter_by_location_and_price(self):
        results = self.customer.search_properties(self.properties, location="Derby", max_price=250000)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].property_id, 1)

    def test_no_match_returns_empty(self):
        results = self.customer.search_properties(self.properties, location="London")
        self.assertEqual(results, [])


class TestInquiryNotificationFlow(unittest.TestCase):
    # IT-01 - integration test for the inquiry + notification flow

    def setUp(self):
        Log().clear()

    def test_inquiry_logs_and_notification(self):
        customer = Customer(20, "buyer@example.com", "buyerpass")
        inquiry = Inquiry(900, customer.user_id, 55, "Is this still available?")
        customer.submit_inquiry(inquiry)

        notif = Notification(300, customer.user_id, "Inquiry", "Inquiry received")
        notif.send_notification()

        action_types = [entry["action_type"] for entry in Log().view_logs()]
        self.assertIn("InquirySubmitted", action_types)
        self.assertIn("Notification", action_types)


class TestPaymentLoggingFlow(unittest.TestCase):
    # IT-02 - integration test for the payment + logging flow

    def setUp(self):
        Log().clear()

    def test_payment_logs_transaction(self):
        customer = Customer(30, "payer@example.com", "payerpass")
        payment = Payment(800, customer.user_id, 50.00, "CreditCard")

        success = customer.make_payment(payment)
        self.assertTrue(success)
        self.assertTrue(payment.confirm_payment())

        payment_logs = [e for e in Log().view_logs() if e["action_type"] == "Payment"]
        self.assertEqual(len(payment_logs), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
