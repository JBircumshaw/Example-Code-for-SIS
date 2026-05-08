from log_singleton import Log


class Inquiry:
    def __init__(self, inquiry_id, user_id, property_id, message):
        self.inquiry_id = inquiry_id
        self.user_id = user_id
        self.property_id = property_id
        self.message = message
        self.status = "Pending"

    def submit(self):
        Log().create_log("InquirySubmitted", f"Inquiry {self.inquiry_id} from user {self.user_id}")

    def update_status(self, new_status):
        self.status = new_status
        Log().create_log("InquiryUpdated", f"Inquiry {self.inquiry_id} -> {new_status}")

    def notify_css(self):
        Log().create_log("CSSNotified", f"CSS notified about inquiry {self.inquiry_id}")
