import unittest
from app.models.place import Place
from app.persistence.repository import InMemoryRepository
from app.models.review import Review
from decimal import Decimal
import math

class TestPlace(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        Place.repository = self.repository
        self.valid_params = {
            'name': 'Cozy Cottage',
            'description': 'A beautiful cottage in the countryside',
            'number_rooms': 3,
            'number_bathrooms': 2,
            'max_guest': 5,
            'price_by_night': 100.50,
            'latitude': 45.5,
            'longitude': -73.5,
            'owner_id': '68f18302-34ef-4189-9259-d9e1a669c73e',
            'city': 'Montreal',
            'country': 'Canada'
        }
        self.place = Place.create(**self.valid_params)

    def tearDown(self):
        Place.repository = InMemoryRepository()

    def test_create(self):
        new_place = Place.create(**self.valid_params)
        self.assertIsInstance(new_place, Place)
        self.assertIn(new_place.id, self.repository._storage)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['max_guest'] = 'invalid'
        with self.assertRaises(ValueError):
            Place.create(**invalid_params)

    def test_get_by_id(self):
        place = Place.get_by_id(self.place.id)
        self.assertEqual(place.id, self.place.id)

    def test_get_by_id_nonexistent(self):
        with self.assertRaises(ValueError):
            Place.get_by_id('nonexistent_id')

    def test_get_all(self):
        places = Place.get_all()
        self.assertIn(self.place, places)

    def test_update(self):
        self.place.update({'name': 'Updated Cottage', 'max_guest': 6, 'price_by_night': 120.75})
        self.assertEqual(self.place.name, 'Updated Cottage')
        self.assertEqual(self.place.max_guest, 6)
        self.assertEqual(self.place.price_by_night, 120.75)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError) as context:
            self.place.update({'invalid_param': 'invalid_value'})
        self.assertIn("Invalid attribute", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.place.update({'max_guest': -1})
        self.assertIn("must be a valid positive integer", str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.place.update({'latitude': 100})
        self.assertIn("must be a number between -90 and 90", str(context.exception))

    def test_delete(self):
        place_id = self.place.id
        self.place.delete()
        with self.assertRaises(ValueError):
            Place.get_by_id(place_id)

    def test_to_dict(self):
        place_dict = self.place.to_dict()
        self.assertIsInstance(place_dict, dict)
        self.assertIn('id', place_dict)
        self.assertIn('name', place_dict)
        self.assertIn('created_at', place_dict)
        self.assertIn('updated_at', place_dict)

    def test_add_remove_amenity(self):
        amenity_id = "test_amenity_id"
        self.place.add_amenity_id(amenity_id)
        self.assertIn(amenity_id, self.place.amenity_ids)
        self.place.remove_amenity_id(amenity_id)
        self.assertNotIn(amenity_id, self.place.amenity_ids)

    def test_add_remove_review(self):
        review_id = "test_review_id"
        self.place.add_review_id(review_id)
        self.assertIn(review_id, self.place.review_ids)
        self.place.remove_review_id(review_id)
        self.assertNotIn(review_id, self.place.review_ids)

    def test_get_by_price_range(self):
        place1 = Place.create(**{**self.valid_params, 'price_by_night': 50})
        place2 = Place.create(**{**self.valid_params, 'price_by_night': 100})
        place3 = Place.create(**{**self.valid_params, 'price_by_night': 150})
        
        results = Place.get_by_price_range(75, 125)
        self.assertIn(place2, results)
        self.assertNotIn(place1, results)
        self.assertNotIn(place3, results)

    def test_get_by_capacity(self):
        place1 = Place.create(**{**self.valid_params, 'max_guest': 2})
        place2 = Place.create(**{**self.valid_params, 'max_guest': 4})
        place3 = Place.create(**{**self.valid_params, 'max_guest': 6})
        
        results = Place.get_by_capacity(4)
        self.assertIn(place2, results)
        self.assertIn(place3, results)
        self.assertNotIn(place1, results)

    def test_get_by_location(self):
        place1 = Place.create(**{**self.valid_params, 'latitude': 48.8566, 'longitude': 2.3522})  # Paris
        place2 = Place.create(**{**self.valid_params, 'latitude': 51.5074, 'longitude': -0.1278})  # London
        
        results = Place.get_by_location(48.8566, 2.3522, 10)  # 10 km radius
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

    def test_calculate_average_rating(self):
        Review.create(place_id=self.place.id, user_id='user1', text='Great place to stay!', rating=5)
        Review.create(place_id=self.place.id, user_id='user2', text='Good experience overall.', rating=4)
        
        self.assertEqual(self.place.calculate_average_rating(), 4.5)

    def test_get_top_rated(self):
        place1 = Place.create(**self.valid_params)
        place2 = Place.create(**self.valid_params)
        place3 = Place.create(**self.valid_params)
        
        Review.create(place_id=place1.id, user_id='user1', text='Excellent place to stay!', rating=5)
        Review.create(place_id=place2.id, user_id='user2', text='Good experience overall.', rating=4)
        Review.create(place_id=place3.id, user_id='user3', text='Average accommodation.', rating=3)
        
        top_rated = Place.get_top_rated(2)
        self.assertEqual(len(top_rated), 2)
        self.assertEqual(top_rated[0].id, place1.id)
        self.assertEqual(top_rated[1].id, place2.id)

    def test_search(self):
        place1 = Place.create(**{**self.valid_params, 'name': 'Cozy Cottage', 'city': 'Paris'})
        place2 = Place.create(**{**self.valid_params, 'name': 'Luxury Apartment', 'city': 'London'})
        
        results = Place.search('cozy')
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)
        
        results = Place.search('london')
        self.assertIn(place2, results)
        self.assertNotIn(place1, results)

    def test_get_by_rating(self):
        place1 = Place.create(**self.valid_params)
        place2 = Place.create(**self.valid_params)
        
        Review.create(place_id=place1.id, user_id='user1', text='Excellent place to stay!', rating=5)
        Review.create(place_id=place2.id, user_id='user2', text='Good experience overall.', rating=4)
        
        results = Place.get_by_rating(4.5)
        self.assertIn(place1, results['matching'])
        self.assertIn(place2, results['suggestions'])

    def test_get_by_city(self):
        place1 = Place.create(**{**self.valid_params, 'city': 'Paris'})
        place2 = Place.create(**{**self.valid_params, 'city': 'London'})
        
        results = Place.get_by_city('Paris')
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

    def test_get_by_country(self):
        place1 = Place.create(**{**self.valid_params, 'country': 'France'})
        place2 = Place.create(**{**self.valid_params, 'country': 'UK'})
        
        results = Place.get_by_country('France')
        self.assertIn(place1, results)
        self.assertNotIn(place2, results)

if __name__ == '__main__':
    unittest.main()