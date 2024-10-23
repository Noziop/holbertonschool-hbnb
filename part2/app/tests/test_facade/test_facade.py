"""Test module for HBnBFacade. Where all spirits come together! 👻"""
import unittest
import uuid
from datetime import datetime
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.placeamenity import PlaceAmenity


class TestHBnBFacade(unittest.TestCase):
    """Test our haunted facade! Where all the magic happens! 🔮"""

    def setUp(self):
        """Prepare our supernatural testing ground! 🏚️"""
        self.facade = HBnBFacade()
        self.unique_id = str(uuid.uuid4())[:6]
        
        # Create our test spirits
        self.user_data = {
            'username': f'Ghost_{self.unique_id}',
            'email': f'ghost_{self.unique_id}@haunted.com',
            'password': 'Haunted123!',
            'first_name': 'Spooky',
            'last_name': 'Spirit'
        }
        self.user = self.facade.create_user(self.user_data)
        
        self.place_data = {
            'name': f'Haunted_Manor_{self.unique_id}',
            'description': 'Where spirits come to rest',
            'number_rooms': 13,
            'number_bathrooms': 4,
            'max_guest': 666,
            'price_by_night': 99.99,
            'latitude': 13.13,
            'longitude': 66.6,
            'owner_id': self.user.id
        }
        self.place = self.facade.create_place(self.place_data)
        
        self.amenity_data = {
            'name': f'Ghost_WiFi_{self.unique_id}',
            'description': 'Supernatural connectivity'
        }
        self.amenity = self.facade.create_amenity(self.amenity_data)
        
        self.review_data = {
            'place_id': self.place.id,
            'user_id': self.user.id,
            'text': 'Perfectly haunted, would ghost again!',
            'rating': 5
        }
        self.review = self.facade.create_review(self.review_data)

    def test_user_operations(self):
        """Test all user operations. Managing our ghostly users! 👻"""
        # Test create and get
        user = self.facade.get_user(self.user.id)
        self.assertEqual(user.username, self.user_data['username'])
        
        # Test update
        updated = self.facade.update_user(user.id, {'first_name': 'Super Spooky'})
        self.assertEqual(updated.first_name, 'Super Spooky')
        
        # Test find
        found = self.facade.find_users(first_name='Super Spooky')
        self.assertIn(updated, found)

    def test_place_operations(self):
        """Test all place operations. Managing our haunted properties! 🏚️"""
        
        # Test create and get
        place = self.facade.get_place(self.place.id)
        self.assertEqual(place.name, self.place_data['name'])
        self.assertEqual(place.price_by_night, self.place_data['price_by_night'])
        
        # Test update
        update_data = {
            'name': f'Super_Haunted_Manor_{self.unique_id}',
            'price_by_night': 666.66,
            'status': 'maintenance'
        }
        updated = self.facade.update_place(place.id, update_data)
        self.assertEqual(updated.name, update_data['name'])
        self.assertEqual(updated.price_by_night, update_data['price_by_night'])
        
        # Test find by price range
        price_results = self.facade.filter_by_price(600.0, 700.0)
        self.assertIn(updated, price_results)
        
        # Test find by location
        location_results = self.facade.get_places_by_location(
            latitude=13.13,
            longitude=66.6,
            radius=10.0
        )
        self.assertIn(updated, location_results)
        
        # Test invalid operations
        with self.assertRaises(ValueError):
            self.facade.create_place({
                **self.place_data,
                'latitude': 91  # Invalid latitude
            })
        
        with self.assertRaises(ValueError):
            self.facade.update_place(place.id, {
                'status': 'super_haunted'  # Invalid status
            })
        
        # Test delete
        self.assertTrue(self.facade.delete_place(place.id))
        with self.assertRaises(ValueError):
            self.facade.get_place(place.id)

    def test_review_operations(self):
        """Test all review operations. Rating our haunted properties! ⭐"""
        
        # Test create and get
        review = self.facade.get_review(self.review.id)
        self.assertEqual(review.text, self.review_data['text'])
        self.assertEqual(review.rating, self.review_data['rating'])
        
        # Test update
        update_data = {
            'text': 'The ghosts were extra friendly tonight! Best haunting ever!',
            'rating': 4
        }
        updated = self.facade.update_review(review.id, update_data)
        self.assertEqual(updated.text, update_data['text'])
        self.assertEqual(updated.rating, update_data['rating'])
        
        # Test get place reviews and rating
        place_reviews = self.facade.get_place_reviews(self.place.id)
        self.assertIn(updated, place_reviews)
        
        avg_rating = self.facade.get_place_rating(self.place.id)
        self.assertEqual(avg_rating, 4.0)  # Notre seule review a un rating de 4
        
        # Test recent reviews
        recent = self.facade.get_recent_reviews(limit=1)
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0].id, updated.id)
        
        # Test invalid operations
        with self.assertRaises(ValueError):
            self.facade.create_review({
                **self.review_data,
                'rating': 6  # Rating invalide
            })
        
        with self.assertRaises(ValueError):
            self.facade.update_review(review.id, {
                'rating': 0  # Rating invalide
            })
        
        # Test delete
        self.assertTrue(self.facade.delete_review(review.id))
        with self.assertRaises(ValueError):
            self.facade.get_review(review.id)

    def test_amenity_operations(self):
        """Test all amenity operations. Managing our supernatural features! ✨"""
        
        # Test create and get
        amenity = self.facade.get_amenity(self.amenity.id)
        self.assertEqual(amenity.name, self.amenity_data['name'])
        self.assertEqual(amenity.description, self.amenity_data['description'])
        
        # Test update
        update_data = {
            'name': f'Super_Ghost_WiFi_{self.unique_id}',
            'description': 'Now with extra ectoplasm bandwidth!'
        }
        updated = self.facade.update_amenity(amenity.id, update_data)  # Reçoit directement l'amenity
        self.assertEqual(updated.name, update_data['name'])
        self.assertNotEqual(updated.description, update_data['description'])
        
        # Test find amenities
        found = self.facade.find_amenities(name=update_data['name'])
        self.assertIn(updated, found)
        
        # Test place-amenity relationship
        # Add amenity to place
        self.facade.add_amenity_to_place(self.place.id, amenity.id)
        
        # Check if amenity is in place
        place_amenities = self.facade.get_place_amenities(self.place.id)
        self.assertIn(amenity, place_amenities)
        
        # Check if place has amenity
        places_with_amenity = self.facade.get_places_with_amenity(amenity.id)
        self.assertIn(self.place, places_with_amenity)
        
        # Remove amenity from place
        self.facade.remove_amenity_from_place(self.place.id, amenity.id)
        
        # Verify removal
        place_amenities = self.facade.get_place_amenities(self.place.id)
        self.assertNotIn(amenity, place_amenities)
        
        # Test invalid operations
        with self.assertRaises(ValueError):
            self.facade.create_amenity({
                'name': ''  # Empty name not allowed
            })
        
        with self.assertRaises(ValueError):
            self.facade.update_amenity(amenity.id, {
                'name': 'Invalid@Name'  # Invalid characters
            })
        
        # Test delete
        self.assertTrue(self.facade.delete_amenity(amenity.id))
        with self.assertRaises(ValueError):
            self.facade.get_amenity(amenity.id)

    def tearDown(self):
        """Clean up our haunted mess! 🧹"""
        # Clear all repositories
        User.repository._storage.clear()
        Place.repository._storage.clear()
        Amenity.repository._storage.clear()
        Review.repository._storage.clear()
        PlaceAmenity.repository._storage.clear()