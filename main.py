"""
main.py
-------
Demonstration entry point for HomeFinder. Creates a small set of users,
properties and interactions to show the modules working together end to end.
Run with: python main.py
"""

from log_singleton import Log
from user import Customer, Administrator
from property import Property
from favourite import Favourite
from inquiry import Inquiry
from payment import Payment
from notification import Notification


def main():
    log = Log()
    log.clear()  # Start with a clean log for this demo run

    # 1. Create an admin and a customer
    admin = Administrator(user_id=1, email="admin@homefinder.com",
                          password="adminpass")
    customer = Customer(user_id=2, email="alice@example.com",
                        password="alicepass")

    # 2. Admin adds two properties to the system
    properties = []
    p1 = Property(101, "Derby", 250000, "Residential", 3, "Garden, Garage")
    p2 = Property(102, "Nottingham", 180000, "Residential", 2, "Balcony")
    admin.add_property(properties, p1)
    admin.add_property(properties, p2)

    # 3. Customer logs in and searches
    customer.login("alicepass")
    matches = customer.search_properties(properties, location="Derby",
                                         max_price=300000)
    print(f"Search returned {len(matches)} property(ies):")
    for prop in matches:
        print(f"  - {prop.display_details()}")

    # 4. Customer favourites a property and submits an inquiry
    customer.manage_favourites(p1.property_id, action="add")

    inquiry = Inquiry(inquiry_id=501, user_id=customer.user_id,
                      property_id=p1.property_id,
                      message="Could I view this property next Saturday?")
    customer.submit_inquiry(inquiry)

    # 5. Customer makes a premium-service payment
    payment = Payment(payment_id=901, user_id=customer.user_id,
                      amount=29.99, payment_method="CreditCard")
    success = customer.make_payment(payment)
    print(f"Payment success: {success}")

    # 6. Customer receives a notification
    notif = Notification(notification_id=701, user_id=customer.user_id,
                         notification_type="ViewingConfirmation",
                         message="Your viewing has been scheduled.")
    notif.send_notification()

    # 7. Show that the Singleton Log captured every action
    print(f"\nTotal log entries: {len(log.view_logs())}")
    for entry in log.view_logs():
        print(f"  [{entry['action_type']}] {entry['details']}")


if __name__ == "__main__":
    main()
