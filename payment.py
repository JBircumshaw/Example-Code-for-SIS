"""
payment.py
----------
Defines the Payment class - handles transactions for premium services.
Maps to the Payment class in the SDS UML Class Diagram (Fig. 1) and
supports SRS requirement RE-14 (secure payment) and RE-15 (transaction logging).
"""

import datetime
from log_singleton import Log


class Payment:
    """Represents a single financial transaction within HomeFinder."""

    VALID_METHODS = ("CreditCard", "BankTransfer")

    def __init__(self, payment_id: int, user_id: int, amount: float,
                 payment_method: str):
        if amount <= 0:
            raise ValueError("Payment amount must be positive.")
        if payment_method not in self.VALID_METHODS:
            raise ValueError(f"Invalid payment method: {payment_method}. "
                             f"Must be one of {self.VALID_METHODS}.")

        self.payment_id = payment_id
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = "Pending"
        self.payment_date = datetime.datetime.now()

    def process_payment(self) -> bool:
        """Simulate processing this payment via the external banking system.
        Returns True on success, False on failure. Logs the result either way."""
        try:
            # In production this would call the External Banking System
            # described as actor AC-4 in the SRS. For this prototype we
            # treat all positive amounts as successful.
            self.payment_status = "Completed"
            self.log_transaction()
            return True
        except Exception as e:
            self.payment_status = "Failed"
            Log().create_log("PaymentError",
                             f"Payment {self.payment_id} failed: {e}")
            return False

    def confirm_payment(self) -> bool:
        """Return True if the payment has been completed."""
        return self.payment_status == "Completed"

    def log_transaction(self) -> None:
        """Record this transaction in the centralised Log (RE-15)."""
        Log().create_log("Payment",
                         f"Payment {self.payment_id} of £{self.amount} via "
                         f"{self.payment_method} - {self.payment_status}.")
