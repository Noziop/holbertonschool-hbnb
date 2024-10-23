"""Test module for Review class. Time to judge the haunted properties! 👻"""
import unittest
import uuid
from datetime import datetime
from app.models.review import Review
from app.models.user import User
from app.models.place import Place


class TestReview(unittest.TestCase):
    """Test cases for Review class. Rating the supernatural! 🏚️"""

    def setUp(self):
        """Prepare our haunted testing grounds! 🦇"""
        unique_id = str(uuid.uuid4())[:6]
        
        # Summon our test user
        self.user = User.create(
            username=f"Ghost_{unique_id}",
            email=f"ghost_{unique_id}@haunted.com",
            password="Haunted123!",
            first_name="Spooky",
            last_name="Critic"
        )
        
        # Create our haunted place
        self.place = Place.create(
            name="Haunted Manor",
            description="Where spirits come to rest",
            number_rooms=13,
            number_bathrooms=4,
            max_guest=666,
            price_by_night=99.99,
            latitude=13.13,
            longitude=66.6,
            owner_id=self.user.id
        )
        
        # Our spectral review data
        self.test_data = {
            'place_id': self.place.id,
            'user_id': self.user.id,
            'text': "The ghosts were very polite, would haunt again! 👻",
            'rating': 5
        }
        
        # Create our haunted review
        self.review = Review.create(**self.test_data)

    def test_initialization(self):
        """Test Review initialization. Summoning a new critique! 👻"""
        self.assertEqual(self.review.text, self.test_data['text'])
        self.assertEqual(self.review.rating, 5)
        
        # Test when the spirits reject the review
        with self.assertRaises(ValueError):
            Review.create(**{
                **self.test_data,
                'text': "2spooky"  # Too short for the spirits!
            })

    def test_rating_validation(self):
        """Test rating validation. The spirits demand proper scores! 🌟"""
        cursed_ratings = [
            0,  # Too low for our haunted standards
            6,  # Even ghosts only count to 5
            "boo",  # Spirits prefer numbers
            3.5,  # Ghosts don't do fractions
            None  # The void is not a rating
        ]
        
        for rating in cursed_ratings:
            with self.assertRaises(ValueError):
                Review.create(**{
                    **self.test_data,
                    'rating': rating
                })

    def test_recent_reviews(self):
        """Test recent reviews. Fresh haunting reports! 👻"""
        # Create multiple spectral reviews
        for i in range(3):
            Review.create(**{
                **self.test_data,
                'text': f"Haunting report #{i}: Excellent ghost activity! {'👻' * i}"
            })
        
        recent = Review.get_recent_reviews(limit=2)
        self.assertEqual(len(recent), 2)
        self.assertTrue(
            recent[0].created_at >= recent[1].created_at
        )

    def test_update(self):
        """Test update functionality. Even ghosts change their minds! 👻"""
        update_data = {
            'text': "Update: The ghosts now serve breakfast! ☕",
            'rating': 4
        }
        
        updated = self.review.update(update_data)
        self.assertEqual(updated.text, update_data['text'])
        self.assertEqual(updated.rating, 4)
        
        # Test invalid updates
        with self.assertRaises(ValueError):
            self.review.update({'rating': 6})  # Too high, even for spirits!
        with self.assertRaises(ValueError):
            self.review.update({'text': 'boo'})  # Ghosts are more eloquent!

    def tearDown(self):
        """Clean up our haunted test environment! 🧹"""
        Review.repository._storage.clear()
        User.repository._storage.clear()
        Place.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()