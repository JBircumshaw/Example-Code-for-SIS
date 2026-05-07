import datetime


class User:
    def __init__(self, user_ID: int, email: str, password: str, role: str):
        self.user_ID = user_ID
        self.email = email
        self.password = password
        self.role = role

    def login(self):
        pass

    def logout(self):
        pass

    def authenticate(self):
        pass


class Customer(User):
    def search_properties(self):
        pass

    def manage_favourites(self):
        pass

    def submit_inquiry(self):
        pass

    def schedule_viewing(self):
        pass

    def make_payment(self):
        pass

    def subscribe_to_alerts(self):
        pass


class CustomerServiceSupervisor(User):
    def manage_inquiries(self):
        pass

    def view_monthly_reports(self):
        pass

    def view_search_trends(self):
        pass


class Administrator(User):
    def add_property(self):
        pass

    def update_property(self):
        pass

    def manage_interactions(self):
        pass


class Property:
    def __init__(self, property_ID: int, location: str, price: float, property_type: str, bedrooms: int, amenities: str, availability_status: str):
        self.property_ID = property_ID
        self.location = location
        self.price = price
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.amenities = amenities
        self.availability_status = availability_status

    def display_details(self):
        pass

    def update_property(self):
        pass

    def check_availability(self):
        pass


class Inquiry:
    def __init__(self, inquiry_ID: int, user_ID: int, property_ID: int, message: str, preferredDate: datetime.date, status: str, dateSubmitted: datetime.datetime):
        self.inquiry_ID = inquiry_ID
        self.user_ID = user_ID
        self.property_ID = property_ID
        self.message = message
        self.preferredDate = preferredDate
        self.status = status
        self.dateSubmitted = dateSubmitted

    def submit_inquiry(self):
        pass

    def update_status(self):
        pass

    def notify_css(self):
        pass


class Report:
    def __init__(self, report_ID: int, user_ID: int, reportMonth: str, generated_date: datetime.datetime, report_type: str):
        self.report_ID = report_ID
        self.user_ID = user_ID
        self.reportMonth = reportMonth
        self.generated_date = generated_date
        self.report_type = report_type

    def generate_report(self):
        pass

    def view_report(self):
        pass


class Favourite:
    def __init__(self, favourite_ID: int, user_ID: int, property_ID: int, dateAdded: datetime.datetime):
        self.favourite_ID = favourite_ID
        self.user_ID = user_ID
        self.property_ID = property_ID
        self.dateAdded = dateAdded

    def add_favourite(self):
        pass

    def remove_favourite(self):
        pass


class Viewing:
    def __init__(self, viewing_ID: int, user_ID: int, property_ID: int, viewing_date: datetime.date, status: str):
        self.viewing_ID = viewing_ID
        self.user_ID = user_ID
        self.property_ID = property_ID
        self.viewing_date = viewing_date
        self.status = status

    def schedule_viewing(self):
        pass

    def cancel_viewing(self):
        pass


class Notification:
    def __init__(self, notification_ID: int, user_ID: int, notification_type: str, message: str, status: str, date_sent: datetime.datetime):
        self.notification_ID = notification_ID
        self.user_ID = user_ID
        self.notification_type = notification_type
        self.message = message
        self.status = status
        self.date_sent = date_sent

    def send_notification(self):
        pass

    def send_property_alert(self):
        pass

    def send_viewing_confirmation(self):
        pass


class Payment:
    def __init__(self, payment_ID: int, user_ID: int, amount: float, payment_method: str, payment_status: str, payment_date: datetime.datetime):
        self.payment_ID = payment_ID
        self.user_ID = user_ID
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.payment_date = payment_date

    def process_payment(self):
        pass

    def confirm_payment(self):
        pass

    def log_transaction(self):
        pass


class Log:
    def __init__(self, log_ID: int, user_ID: int, action_type: str, timestamp: datetime.datetime, details: str):
        self.log_ID = log_ID
        self.user_ID = user_ID
        self.action_type = action_type
        self.timestamp = timestamp
        self.details = details

    def create_log(self):
        pass

    def view_logs(self):
        pass