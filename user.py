"""
user.py
-------
Defines the User base class and its three role-specific subclasses
(Customer, CustomerServiceSupervisor, Administrator) for HomeFinder.
Maps to the User-hierarchy section of the UML Class Diagram (SDS Fig. 1)
and satisfies SRS requirements RE-1 (account creation) and RE-11 (three roles).
"""

from log_singleton import Log


class User:
    """Base class representing any HomeFinder user account (RE-1, RE-11)."""

    def __init__(self, user_id: int, email: str, password: str, role: str):
        # Basic input validation - prevents creation of malformed accounts
        if not email or "@" not in email:
            raise ValueError("Invalid email address provided.")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters.")
        if role not in ("Customer", "CSS", "Administrator"):
            raise ValueError(f"Unknown role: {role}")

        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.is_logged_in = False

    def login(self, password_attempt: str) -> bool:
        """Attempt to log the user in. Returns True if successful."""
        try:
            if password_attempt == self.password:
                self.is_logged_in = True
                Log().create_log("Login", f"User {self.user_id} logged in.")
                return True
            Log().create_log("LoginFailed", f"User {self.user_id} login failed.")
            return False
        except Exception as e:
            # Defensive logging in case password comparison fails unexpectedly
            Log().create_log("Error", f"Login error for {self.user_id}: {e}")
            return False

    def logout(self) -> None:
        """Log the user out and record the action."""
        self.is_logged_in = False
        Log().create_log("Logout", f"User {self.user_id} logged out.")

    def authenticate(self) -> bool:
        """Return whether the user is currently authenticated."""
        return self.is_logged_in


class Customer(User):
    """Customer user - browses properties, makes inquiries, and pays for services."""

    def __init__(self, user_id: int, email: str, password: str):
        super().__init__(user_id, email, password, "Customer")
        self.favourites = []  # List of property IDs the customer has saved
        self.subscriptions = []  # Property types/locations subscribed for alerts

    def search_properties(self, properties: list, location: str = None,
                          max_price: float = None) -> list:
        """Filter a list of Property objects by location and price (RE-6)."""
        if not isinstance(properties, list):
            raise TypeError("properties must be a list of Property objects.")

        results = []
        for prop in properties:
            if location and prop.location.lower() != location.lower():
                continue
            if max_price is not None and prop.price > max_price:
                continue
            results.append(prop)

        Log().create_log("Search",
                         f"Customer {self.user_id} searched "
                         f"location={location}, max_price={max_price}.")
        return results

    def manage_favourites(self, property_id: int, action: str = "add") -> None:
        """Add or remove a property from the customer's favourites list (RE-7)."""
        if action == "add" and property_id not in self.favourites:
            self.favourites.append(property_id)
        elif action == "remove" and property_id in self.favourites:
            self.favourites.remove(property_id)
        else:
            raise ValueError(f"Invalid favourites action: {action}")

        Log().create_log("Favourite",
                         f"Customer {self.user_id} {action} property {property_id}.")

    def submit_inquiry(self, inquiry) -> None:
        """Submit an inquiry against a property (RE-9)."""
        inquiry.submit()
        Log().create_log("Inquiry",
                         f"Customer {self.user_id} submitted inquiry "
                         f"{inquiry.inquiry_id}.")

    def schedule_viewing(self, viewing) -> None:
        """Schedule a property viewing (RE-9)."""
        viewing.status = "Scheduled"
        Log().create_log("Viewing",
                         f"Customer {self.user_id} scheduled viewing "
                         f"{viewing.viewing_id}.")

    def make_payment(self, payment) -> bool:
        """Process a payment for premium services (RE-14)."""
        try:
            return payment.process_payment()
        except Exception as e:
            Log().create_log("PaymentError",
                             f"Customer {self.user_id} payment failed: {e}")
            return False

    def subscribe_to_alerts(self, property_type: str, location: str) -> None:
        """Subscribe to property alerts for similar listings (RE-10)."""
        self.subscriptions.append({"type": property_type, "location": location})
        Log().create_log("Subscribe",
                         f"Customer {self.user_id} subscribed to "
                         f"{property_type} in {location}.")


class CustomerServiceSupervisor(User):
    """Supervisor account - handles inquiries and views reports."""

    def __init__(self, user_id: int, email: str, password: str):
        super().__init__(user_id, email, password, "CSS")

    def manage_inquiries(self, inquiries: list) -> list:
        """Return a list of all currently pending inquiries."""
        return [i for i in inquiries if i.status == "Pending"]

    def view_monthly_reports(self, reports: list, month: str) -> list:
        """Return reports filtered by month (RE-12)."""
        return [r for r in reports if r.report_month == month]

    def view_search_trends(self) -> list:
        """Return all logged search actions for trend analysis (RE-12)."""
        all_logs = Log().view_logs()
        return [entry for entry in all_logs if entry["action_type"] == "Search"]


class Administrator(User):
    """Administrator account - manages property listings and oversees users (RE-13)."""

    def __init__(self, user_id: int, email: str, password: str):
        super().__init__(user_id, email, password, "Administrator")

    def add_property(self, properties: list, new_property) -> None:
        """Add a new property listing to the system."""
        properties.append(new_property)
        Log().create_log("AddProperty",
                         f"Admin {self.user_id} added property "
                         f"{new_property.property_id}.")

    def update_property(self, target_property, **changes) -> None:
        """Update fields on an existing property listing."""
        for key, value in changes.items():
            if hasattr(target_property, key):
                setattr(target_property, key, value)
            else:
                raise AttributeError(f"Property has no field '{key}'.")
        Log().create_log("UpdateProperty",
                         f"Admin {self.user_id} updated property "
                         f"{target_property.property_id}.")

    def manage_interactions(self, inquiries: list) -> int:
        """Returns count of inquiries currently being managed (RE-13)."""
        return len(inquiries)
