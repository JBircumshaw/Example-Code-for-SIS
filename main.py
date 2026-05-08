from log_singleton import Log
from user import Customer, Administrator
from property import Property
from inquiry import Inquiry
from payment import Payment
from notification import Notification


# Set up users
admin = Administrator(1, "admin@homefinder.com", "adminpass")
customer = Customer(2, "alice@example.com", "alicepass")

# Admin adds two properties
properties = []
p1 = Property(101, "Derby", 250000, "Residential", 3, "Garden, Garage")
p2 = Property(102, "Nottingham", 180000, "Residential", 2, "Balcony")
admin.add_property(properties, p1)
admin.add_property(properties, p2)

# Customer logs in and searches
customer.login("alicepass")
matches = customer.search_properties(properties, location="Derby", max_price=300000)

print(f"Found {len(matches)} properties:")
for prop in matches:
    print(prop.display_details())

# Customer submits an inquiry
inquiry = Inquiry(501, customer.user_id, p1.property_id, "Can I view this property?")
customer.submit_inquiry(inquiry)

# Customer makes a payment
payment = Payment(901, customer.user_id, 29.99, "CreditCard")
customer.make_payment(payment)

# Customer gets a notification
notif = Notification(701, customer.user_id, "ViewingConfirmation", "Viewing scheduled")
notif.send_notification()

# Show all logs
print(f"\nLog entries: {len(Log().view_logs())}")
for entry in Log().view_logs():
    print(f"  [{entry['action_type']}] {entry['details']}")
