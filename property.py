from log_singleton import Log


class Property:
    def __init__(self, property_id, location, price, property_type, bedrooms, amenities):
        self.property_id = property_id
        self.location = location
        self.price = price
        self.property_type = property_type
        self.bedrooms = bedrooms
        self.amenities = amenities
        self.availability_status = "Available"

    def display_details(self):
        return f"Property {self.property_id}: {self.property_type} in {self.location}, £{self.price}, {self.bedrooms} bed"

    def update_property(self, field, value):
        setattr(self, field, value)
        Log().create_log("PropertyUpdate", f"Property {self.property_id} updated")

    def check_availability(self):
        return self.availability_status == "Available"
