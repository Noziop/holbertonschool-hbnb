from .basemodel import BaseModel

class PlaceAmenity(BaseModel):
    def __init__(self, place_id, amenity_id):
        super().__init__()
        self.place_id = place_id
        self.amenity_id = amenity_id

    def to_dict(self):
        place_amenity_dict = super().to_dict()
        place_amenity_dict.update({
            'place_id': self.place_id,
            'amenity_id': self.amenity_id
        })
        return place_amenity_dict