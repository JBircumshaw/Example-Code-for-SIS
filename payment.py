from log_singleton import Log


class Payment:
    def __init__(self, payment_id, user_id, amount, payment_method):
        self.payment_id = payment_id
        self.user_id = user_id
        self.amount = amount
        self.payment_method = payment_method
        self.status = "Pending"

    def process_payment(self):
        if self.amount <= 0:
            self.status = "Failed"
            return False
        self.status = "Completed"
        self.log_transaction()
        return True

    def confirm_payment(self):
        return self.status == "Completed"

    def log_transaction(self):
        Log().create_log("Payment", f"Payment {self.payment_id} of £{self.amount} - {self.status}")
