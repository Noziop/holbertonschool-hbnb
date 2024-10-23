"""Test module for Review class. Time to judge the judge! 💅"""
import unittest
from datetime import datetime
from app.models.review import Review
from app.models.user import User
from app.models.place import Place


class TestReview(unittest.TestCase):
    """Test cases for Review class. Spilling the testing tea! ☕"""

    def setUp(self):
        """Set up test cases. Preparing the stage! 🎭"""
        # Create test user
        self.user = User.create(
            username="CriticQueen",
            email="critic@test.com",
            password="Password123!",
            first_name="Sassy",
            last_name="Critic"
        )
        
        # Create test place
        self.place = Place.create(
            name="Fabulous Hotel",
            description="A place to serve looks",
            number_rooms=1,
            number_bathrooms=1,
            max_guest=2,
            price_by_night=100.0,
            latitude=0.0,
            longitude=0.0,
            owner_id=self.user.id
        )
        
        # Review test data
        self.test_data = {
            'place_id': self.place.id,
            'user_id': self.user.id,
            'text': "This place is serving looks! Totally fabulous!",
            'rating': 5
        }
        
        self.review = Review.create(**self.test_data)

    def test_initialization(self):
        """Test Review initialization. Birth of a critique! 👶"""
        self.assertEqual(self.review.text, self.test_data['text'])
        self.assertEqual(self.review.rating, 5)
        
        # Test validation errors
        with self.assertRaises(ValueError):
            Review.create(**{
                **self.test_data,
                'text': "Too short"  # < 10 chars
            })
        with self.assertRaises(ValueError):
            Review.create(**{
                **self.test_data,
                'rating': 6  # > 5
            })

    def test_rating_validation(self):
        """Test rating validation. Numbers only, honey! 🔢"""
        invalid_ratings = [
            0,  # Too low
            6,  # Too high
            "five",  # Not a number
            3.5,  # Must be integer
            None  # Must have value
        ]
        
        for rating in invalid_ratings:
            with self.assertRaises(ValueError):
                Review.create(**{
                    **self.test_data,
                    'rating': rating
                })

    def test_get_by_methods(self):
        """Test get_by methods. Finding tea everywhere! 🔍"""
        # Test get_by_place
        place_reviews = Review.get_by_place(self.place.id)
        self.assertTrue(isinstance(place_reviews, list))
        self.assertEqual(len(place_reviews), 1)
        self.assertEqual(place_reviews[0].id, self.review.id)
        
        # Test get_by_user
        user_reviews = Review.get_by_user(self.user.id)
        self.assertTrue(isinstance(user_reviews, list))
        self.assertEqual(len(user_reviews), 1)
        self.assertEqual(user_reviews[0].id, self.review.id)

    def test_average_rating(self):
        """Test average rating. Math but make it fashion! ✨"""
        # Add another review
        Review.create(**{
            **self.test_data,
            'rating': 4,
            'text': "Almost perfect, like my ex's excuse!"
        })
        
        avg = Review.get_average_rating(self.place.id)
        self.assertEqual(avg, 4.5)

    def test_recent_reviews(self):
        """Test recent reviews. Hot off the press! 🗞️"""
        # Create multiple reviews
        for i in range(3):
            Review.create(**{
                **self.test_data,
                'text': f"Review number {i} is serving! {'✨' * i}"
            })
        
        recent = Review.get_recent_reviews(limit=2)
        self.assertEqual(len(recent), 2)
        self.assertTrue(
            recent[0].created_at >= recent[1].created_at
        )

    def test_update(self):
        """Test update functionality. Changed our mind! 💅"""
        update_data = {
            'text': "Updated my mind, still fabulous though!",
            'rating': 4
        }
        
        updated = self.review.update(update_data)
        self.assertEqual(updated.text, update_data['text'])
        self.assertEqual(updated.rating, 4)
        
        # Test invalid updates
        with self.assertRaises(ValueError):
            self.review.update({'rating': 6})
        with self.assertRaises(ValueError):
            self.review.update({'text': 'too short'})

    def tearDown(self):
        """Clean up after tests. Leave no traces! 🧹"""
        Review.repository._storage.clear()
        User.repository._storage.clear()
        Place.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()