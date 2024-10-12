from .base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        amenity_dict = super().to_dict()
        amenity_dict.update({
            'name': self.name
        })
        return amenity_dict