from log_singleton import Log


class Notification:
    def __init__(self, notification_id, user_id, notification_type, message):
        self.notification_id = notification_id
        self.user_id = user_id
        self.notification_type = notification_type
        self.message = message
        self.status = "Pending"

    def send_notification(self):
        self.status = "Sent"
        Log().create_log("Notification", f"Notification {self.notification_id} sent to user {self.user_id}")

    def send_property_alert(self):
        self.notification_type = "PropertyAlert"
        self.send_notification()

    def send_viewing_confirmation(self):
        self.notification_type = "ViewingConfirmation"
        self.send_notification()
