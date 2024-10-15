import unittest
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class TestReview(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Review.repository = self.repository
        self.valid_params = {
            'place_id': 'place123',
            'user_id': 'user456',
            'text': 'This is a great place to stay!',
            'rating': 5
        }
        self.review = Review.create(**self.valid_params)

    def tearDown(self):
        Review.repository = InMemoryRepository()

    def test_create(self):
        new_review = Review.create(**self.valid_params)
        self.assertIsInstance(new_review, Review)
        self.assertEqual(new_review.place_id, 'place123')
        self.assertEqual(new_review.user_id, 'user456')
        self.assertEqual(new_review.text, 'This is a great place to stay!')
        self.assertEqual(new_review.rating, 5)
        self.assertIn(new_review.id, self.repository._storage)

    def test_update(self):
        update_data = {'text': 'Updated review text', 'rating': 4}
        self.review.update(update_data)
        self.assertEqual(self.review.text, 'Updated review text')
        self.assertEqual(self.review.rating, 4)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.review.update({'invalid_param': 'value'})

    def test_invalid_rating(self):
        with self.assertRaises(ValueError):
            Review.create(**{**self.valid_params, 'rating': 6})
        with self.assertRaises(ValueError):
            Review.create(**{**self.valid_params, 'rating': 0})
        with self.assertRaises(ValueError):
            Review.create(**{**self.valid_params, 'rating': 'not a number'})

    def test_invalid_text(self):
        with self.assertRaises(ValueError):
            Review.create(**{**self.valid_params, 'text': 'Too short'})

    def test_invalid_place_id(self):
        with self.assertRaises(ValueError):
            Review.create(**{**self.valid_params, 'place_id': ''})

    def test_invalid_user_id(self):
        with self.assertRaises(ValueError):
            Review.create(**{**self.valid_params, 'user_id': ''})

    def test_get_by_place(self):
        reviews = Review.get_by_place('place123')
        self.assertIn(self.review, reviews)

    def test_get_by_user(self):
        reviews = Review.get_by_user('user456')
        self.assertIn(self.review, reviews)

    def test_to_dict(self):
        review_dict = self.review.to_dict()
        self.assertIn('id', review_dict)
        self.assertIn('place_id', review_dict)
        self.assertIn('user_id', review_dict)
        self.assertIn('text', review_dict)
        self.assertIn('rating', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)

    def test_create_with_error(self):
        with self.assertRaises(ValueError):
            Review.create(place_id='', user_id='', text='', rating='invalid')

    def test_get_by_id(self):
        retrieved_review = Review.get_by_id(self.review.id)
        self.assertEqual(retrieved_review.id, self.review.id)

        with self.assertRaises(ValueError):
            Review.get_by_id('non_existent_id')

    def test_delete(self):
        review_id = self.review.id
        self.review.delete()
        self.assertNotIn(review_id, self.repository._storage)

        with self.assertRaises(ValueError):
            Review.get_by_id(review_id)

    def test_update_ids(self):
        new_place_id = "new_place_123"
        new_user_id = "new_user_456"
        self.review.update({
            'place_id': new_place_id,
            'user_id': new_user_id
        })
        self.assertEqual(self.review.place_id, new_place_id)
        self.assertEqual(self.review.user_id, new_user_id)

    def test_update_invalid_place_id(self):
        with self.assertRaises(ValueError):
            self.review.update({'place_id': ''})

    def test_update_invalid_user_id(self):
        with self.assertRaises(ValueError):
            self.review.update({'user_id': ''})

    def test_update_invalid_text(self):
        with self.assertRaises(ValueError):
            self.review.update({'text': 'Too short'})
    
    def test_update_invalid_rating(self):
        with self.assertRaises(ValueError):
            self.review.update({'rating': 6})
        with self.assertRaises(ValueError):
            self.review.update({'rating': 0})
        with self.assertRaises(ValueError):
            self.review.update({'rating': 'not a number'})

if __name__ == '__main__':
    unittest.main()