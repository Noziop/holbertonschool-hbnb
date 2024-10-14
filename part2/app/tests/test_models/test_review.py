
import unittest
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class TestReview(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Review.repository = self.repository
        self.valid_params = {'place_id': '41e1c85e-b474-4aad-bf5e-8468f441d505', 'user_id': '761775dd-dd12-48a1-9b05-7bbb6dd69320', 'text': 'Cut left there radio threat. Call partner exist stuff wide.', 'rating': 'land'}
        self.review = Review(**self.valid_params)

    def tearDown(self):
        Review.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['repository']
        for attr in attrs:
            self.assertTrue(hasattr(self.review, attr))

    def test_methods(self):
        methods = ['_validate_id', '_validate_rating', '_validate_text', 'create', 'delete', 'get_all', 'get_by_id', 'get_by_place', 'get_by_user', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.review, method))

    def test_create(self):
        new_review = Review.create(**self.valid_params)
        self.assertIsInstance(new_review, Review)
        self.assertIn(new_review.id, self.repository._storage)

    def test_get_by_id(self):
        review = Review.get_by_id(self.review.id)
        self.assertEqual(review.id, self.review.id)

    def test_update(self):
        update_data = {
            'name': 'Updated Name' if hasattr(self.review, 'name') else None,
            'description': 'Updated Description' if hasattr(self.review, 'description') else None
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        self.review.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.review, key), value)

    def test_to_dict(self):
        review_dict = self.review.to_dict()
        self.assertIsInstance(review_dict, dict)
        self.assertIn('id', review_dict)
        self.assertIn('created_at', review_dict)
        self.assertIn('updated_at', review_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            Review(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.review.update({'invalid_param': 'invalid_value'})

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
