from .base_model import BaseModel

class Review(BaseModel):
    def __init__(self, place_id, user_id, text):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.text = text

    def to_dict(self):
        review_dict = super().to_dict()
        review_dict.update({
            'place_id': self.place_id,
            'user_id': self.user_id,
            'text': self.text
        })
        return review_dict