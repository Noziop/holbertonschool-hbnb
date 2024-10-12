from .basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, name, description, number_rooms, number_bathrooms, max_guest, price_by_night, latitude, longitude, city="", country="", owner_id=None):
        super().__init__()
        self.name = name
        self.description = description
        self.number_rooms = number_rooms
        self.number_bathrooms = number_bathrooms
        self.max_guest = max_guest
        self.price_by_night = price_by_night
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.country = country
        self.owner_id = owner_id
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)

    def set_owner(self, user_id):
        self.user_id = user_id

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def to_dict(self):
        place_dict = super().to_dict()
        place_dict.update({
            'name': self.name,
            'description': self.description,
            'number_rooms': self.number_rooms,
            'number_bathrooms': self.number_bathrooms,
            'max_guest': self.max_guest,
            'price_by_night': self.price_by_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'user_id': self.user_id,
            'amenities': [amenity.id for amenity in self.amenities],
            'reviews': [review.id for review in self.reviews]
        })
        return place_dict