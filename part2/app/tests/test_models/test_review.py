import unittest
from app.models.review import Review
from app.persistence.repository import InMemoryRepository
from datetime import datetime

class TestReview(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Review.repository = self.repository
        self.valid_params = {
            'place_id': '123e4567-e89b-12d3-a456-426614174000',
            'user_id': '98765432-e89b-12d3-a456-426614174000',
            'text': 'This is a great place to stay!',
            'rating': 5
        }
        self.review = Review.create(**self.valid_params)

    def tearDown(self):
        Review.repository = InMemoryRepository()

    def test_create(self):
        new_review = Review.create(**self.valid_params)
        self.assertIsInstance(new_review, Review)
        self.assertIn(new_review.id, self.repository._storage)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['rating'] = 6
        with self.assertRaises(ValueError):
            Review.create(**invalid_params)

    def test_get_by_id(self):
        review = Review.get_by_id(self.review.id)
        self.assertEqual(review.id, self.review.id)

    def test_get_by_id_nonexistent(self):
        with self.assertRaises(ValueError):
            Review.get_by_id('nonexistent_id')

    def test_get_all(self):
        reviews = Review.get_all()
        self.assertIn(self.review, reviews)

    def test_update(self):
        update_data = {
            'text': 'Updated review text',
            'rating': 4
        }
        self.review.update(update_data)
        self.assertEqual(self.review.text, 'Updated review text')
        self.assertEqual(self.review.rating, 4)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.review.update({'invalid_param': 'invalid_value'})
        with self.assertRaises(ValueError):
            self.review.update({'rating': 0})

    def test_delete(self):
        review_id = self.review.id
        self.review.delete()
        with self.assertRaises(ValueError):
            Review.get_by_id(review_id)

    def test_to_dict(self):
        review_dict = self.review.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertIn('id', review_dict)
        self.assertIn('place_id', review_dict)
        self.assertIn('user_id', review_dict)
        self.assertIn('text', review_dict)
        self.assertIn('rating', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)

    def test_get_by_place(self):
        review1 = Review.create(**self.valid_params)
        review2 = Review.create(**{**self.valid_params, 'place_id': 'different_place_id'})
        
        results = Review.get_by_place(self.valid_params['place_id'])
        self.assertIn(review1, results)
        self.assertNotIn(review2, results)

    def test_get_by_user(self):
        review1 = Review.create(**self.valid_params)
        review2 = Review.create(**{**self.valid_params, 'user_id': 'different_user_id'})
        
        results = Review.get_by_user(self.valid_params['user_id'])
        self.assertIn(review1, results)
        self.assertNotIn(review2, results)

    def test_validate_text(self):
        with self.assertRaises(ValueError):
            Review._validate_text("Short")  # Less than 10 characters

    def test_validate_rating(self):
        with self.assertRaises(ValueError):
            Review._validate_rating(0)
        with self.assertRaises(ValueError):
            Review._validate_rating(6)

if __name__ == '__main__':
    unittest.main()