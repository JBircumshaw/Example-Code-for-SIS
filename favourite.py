"""
favourite.py
------------
Defines the Favourite class - represents a property saved to a customer's
favourites list. Maps to the Favourite class in the SDS UML Class Diagram
and supports SRS requirement RE-7.
"""

import datetime
from log_singleton import Log


class Favourite:
    """A single entry in a customer's favourites list."""

    def __init__(self, favourite_id: int, user_id: int, property_id: int):
        self.favourite_id = favourite_id
        self.user_id = user_id
        self.property_id = property_id
        self.date_added = datetime.datetime.now()

    def add_favourite(self) -> None:
        """Record the addition of this favourite via the central log."""
        Log().create_log("FavouriteAdded",
                         f"User {self.user_id} added property {self.property_id}.")

    def remove_favourite(self) -> None:
        """Record the removal of this favourite."""
        Log().create_log("FavouriteRemoved",
                         f"User {self.user_id} removed property {self.property_id}.")
