"""
property.py
-----------
Defines the Property class for HomeFinder, representing a real estate listing.
Maps to the Property class in the SDS UML Class Diagram (Fig. 1) and
supports SRS requirements RE-5 (categorisation) and RE-6 (search/filter).
"""

from log_singleton import Log


class Property:
    """A property listing within HomeFinder."""

    VALID_TYPES = ("residential", "commercial", "rental")

    def __init__(self, property_id: int, location: str, price: float,
                 property_type: str, bedrooms: int, amenities: str,
                 availability_status: str = "Available"):
        if property_type.lower() not in self.VALID_TYPES:
            raise ValueError(f"Invalid property_type. Must be one of "
                             f"{self.VALID_TYPES}")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if bedrooms < 0:
            raise ValueError("Bedrooms cannot be negative.")

        self.property_id = property_id
        self.location = location
        self.price = price
        self.property_type = property_type.lower()
        self.bedrooms = bedrooms
        self.amenities = amenities
        self.availability_status = availability_status

    def display_details(self) -> str:
        """Return a human-readable summary of this property."""
        return (f"Property {self.property_id}: {self.property_type} in "
                f"{self.location}, £{self.price}, {self.bedrooms} bed, "
                f"{self.availability_status}")

    def update_property(self, **changes) -> None:
        """Apply changes to one or more property fields with validation."""
        for key, value in changes.items():
            if not hasattr(self, key):
                raise AttributeError(f"Property has no field '{key}'.")
            setattr(self, key, value)
        Log().create_log("PropertyUpdate",
                         f"Property {self.property_id} updated.")

    def check_availability(self) -> bool:
        """Return True if the property is currently available."""
        return self.availability_status == "Available"
