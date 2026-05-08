from log_singleton import Log


class User:
    def __init__(self, user_id, email, password, role):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.logged_in = False

    def login(self, password_attempt):
        if password_attempt == self.password:
            self.logged_in = True
            Log().create_log("Login", f"User {self.user_id} logged in")
            return True
        return False

    def logout(self):
        self.logged_in = False
        Log().create_log("Logout", f"User {self.user_id} logged out")

    def authenticate(self):
        return self.logged_in


class Customer(User):
    def __init__(self, user_id, email, password):
        super().__init__(user_id, email, password, "Customer")
        self.favourites = []

    def search_properties(self, properties, location=None, max_price=None):
        results = []
        for prop in properties:
            if location and prop.location.lower() != location.lower():
                continue
            if max_price is not None and prop.price > max_price:
                continue
            results.append(prop)

        Log().create_log("Search", f"Customer {self.user_id} searched {location}")
        return results

    def manage_favourites(self, property_id, action):
        if action == "add":
            self.favourites.append(property_id)
        elif action == "remove":
            self.favourites.remove(property_id)
        Log().create_log("Favourite", f"User {self.user_id} {action} {property_id}")

    def submit_inquiry(self, inquiry):
        inquiry.submit()

    def make_payment(self, payment):
        return payment.process_payment()


class CustomerServiceSupervisor(User):
    def __init__(self, user_id, email, password):
        super().__init__(user_id, email, password, "CSS")

    def manage_inquiries(self, inquiries):
        return [i for i in inquiries if i.status == "Pending"]


class Administrator(User):
    def __init__(self, user_id, email, password):
        super().__init__(user_id, email, password, "Administrator")

    def add_property(self, properties, new_property):
        properties.append(new_property)
        Log().create_log("AddProperty", f"Admin added property {new_property.property_id}")
