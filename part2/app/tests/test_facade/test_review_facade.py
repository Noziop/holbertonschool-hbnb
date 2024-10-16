import unittest
from app.services.facade import HBnBFacade
from app.models.review import Review
from app.models.place import Place
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class TestReviewFacade(unittest.TestCase):

    def setUp(self):
        self.facade = HBnBFacade()
        self.user = User.create(username="testuser", email="test@example.com", password="password123")
        self.place = Place.create(name="Test Place", description="Test Description", number_rooms=2, number_bathrooms=1, max_guest=4, price_by_night=100, latitude=45.5, longitude=-73.5, owner_id=self.user.id)
        self.review_data = {
            'place_id': self.place.id,
            'user_id': self.user.id,
            'text': 'Great place to stay!',
            'rating': 5
        }

    def tearDown(self):
        Review.repository = InMemoryRepository()
        Place.repository = InMemoryRepository()
        User.repository = InMemoryRepository()

    def test_create_review_valid(self):
        review = self.facade.create_review(self.review_data)
        self.assertIsInstance(review, Review)
        self.assertEqual(review.text, 'Great place to stay!')
        self.assertEqual(review.rating, 5)

    def test_create_review_invalid_rating(self):
        invalid_data = self.review_data.copy()
        invalid_data['rating'] = 6
        with self.assertRaises(ValueError):
            self.facade.create_review(invalid_data)

    def test_create_review_invalid_text(self):
        invalid_data = self.review_data.copy()
        invalid_data['text'] = 'Short'
        with self.assertRaises(ValueError):
            self.facade.create_review(invalid_data)

    def test_get_review_existing(self):
        created_review = self.facade.create_review(self.review_data)
        retrieved_review = self.facade.get_review(created_review.id)
        self.assertEqual(created_review.id, retrieved_review.id)

    def test_get_review_nonexistent(self):
        with self.assertRaises(ValueError):
            self.facade.get_review('nonexistent_id')

    def test_update_review_valid(self):
        review = self.facade.create_review(self.review_data)
        updated_data = {
            'text': 'Updated review text',
            'rating': 4
        }
        updated_review = self.facade.update_review(review.id, updated_data)
        self.assertEqual(updated_review.text, 'Updated review text')
        self.assertEqual(updated_review.rating, 4)

    def test_update_review_invalid_rating(self):
        review = self.facade.create_review(self.review_data)
        invalid_data = {'rating': 0}
        with self.assertRaises(ValueError):
            self.facade.update_review(review.id, invalid_data)

    def test_update_nonexistent_review(self):
        with self.assertRaises(ValueError):
            self.facade.update_review('nonexistent_id', {'text': 'New text'})

    def test_delete_review(self):
        review = self.facade.create_review(self.review_data)
        self.facade.delete_review(review.id)
        with self.assertRaises(ValueError):
            self.facade.get_review(review.id)

    def test_delete_nonexistent_review(self):
        with self.assertRaises(ValueError):
            self.facade.delete_review('nonexistent_id')

    def test_get_reviews_by_place(self):
        self.facade.create_review(self.review_data)
        reviews = self.facade.get_reviews_by_place(self.place.id)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].place_id, self.place.id)

    def test_get_reviews_by_user(self):
        self.facade.create_review(self.review_data)
        reviews = self.facade.get_reviews_by_user(self.user.id)
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].user_id, self.user.id)

    def test_get_place_average_rating(self):
        self.facade.create_review(self.review_data)
        self.facade.create_review({**self.review_data, 'rating': 4})
        average_rating = self.facade.get_place_average_rating(self.place.id)
        self.assertEqual(average_rating, 4.5)

    def test_get_recent_reviews(self):
        for i in range(10):
            self.facade.create_review({**self.review_data, 'text': f'This is review number {i}. It is long enough.'})
        recent_reviews = self.facade.get_recent_reviews(5)
        self.assertEqual(len(recent_reviews), 5)
        self.assertEqual(recent_reviews[0].text, 'This is review number 9. It is long enough.')

if __name__ == '__main__':
    unittest.main()