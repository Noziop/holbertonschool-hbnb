import uuid

class Place:
    def __init__(self, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.max_guest = max_guest
        self.price_by_night = price_by_night
        self.latitude = latitude
        self.longitude = longitude
        self.amenities = []  # Liste pour stocker les commodités
        self.reviews = []    # Liste pour stocker les avis
        self.user_id = None  # ID de l'utilisateur propriétaire

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)

    def set_owner(self, user_id):
        self.user_id = user_id