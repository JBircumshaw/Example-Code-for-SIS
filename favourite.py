from log_singleton import Log


class Favourite:
    def __init__(self, favourite_id, user_id, property_id):
        self.favourite_id = favourite_id
        self.user_id = user_id
        self.property_id = property_id

    def add_favourite(self):
        Log().create_log("FavouriteAdded", f"User {self.user_id} added property {self.property_id}")

    def remove_favourite(self):
        Log().create_log("FavouriteRemoved", f"User {self.user_id} removed property {self.property_id}")
