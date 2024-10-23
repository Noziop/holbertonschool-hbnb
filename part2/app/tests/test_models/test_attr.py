"""Test module for our haunted models. Let the spooky testing begin! 👻"""
import unittest
import uuid
from datetime import datetime
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class TestHauntedModels(unittest.TestCase):
    """Testing our models like we're ghost hunters! 👻"""

    def setUp(self):
        unique_id = str(uuid.uuid4())[:6]
        self.ghost_hunter = User.create(
            username=f"Ghost_{unique_id}",
            email=f"hunter_{unique_id}@haunted.com",
            password="Pikaboo123!",
            first_name="Ghost",
            last_name="Hunter",
            city="Transylvania"
        )

        self.haunted_mansion = Place.create(
            name="Haunted Mansion",
            description="Very spooky, much wow!",
            number_rooms=13,
            number_bathrooms=4,
            max_guest=666,
            price_by_night=99.99,
            latitude=13.13,
            longitude=66.6,
            owner_id=self.ghost_hunter.id,
            city="Transylvania"
        )

        self.spooky_review = Review.create(
            text="Ghosts were very polite, would haunt again!",
            rating=5,
            user_id=self.ghost_hunter.id,
            place_id=self.haunted_mansion.id
        )

        self.ghost_amenity = Amenity.create(
            name="Friendly Ghost",
            description="Comes with complementary chains!"
        )

    def test_multiple_attrs_single_model(self):
        """Test searching with multiple attributes on one model! 🔍"""
        # Find our ghost hunter using our setUp values
        hunter = User.get_by_attr(
            username=self.ghost_hunter.username,
            city="Transylvania"
        )
        self.assertIsNotNone(hunter)
        self.assertEqual(hunter.email, self.ghost_hunter.email)

        # Find haunted places
        mansion = Place.get_by_attr(
            city="Transylvania",
            number_rooms=13
        )
        self.assertIsNotNone(mansion)
        self.assertEqual(mansion.name, "Haunted Mansion")

    def test_multiple_attrs_multiple_results(self):
        """Test getting multiple results! 👻👻👻"""
        # Create more haunted places
        Place.create(
            name="Ghost Tower",
            description="Very tall, much spook!",
            number_rooms=13,
            number_bathrooms=2,
            max_guest=13,
            price_by_night=66.6,
            latitude=13.13,
            longitude=66.6,
            owner_id=self.ghost_hunter.id,
            city="Transylvania"
        )

        # Find all places with 13 rooms in Transylvania
        haunted_places = Place.get_by_attr(
            multiple=True,
            city="Transylvania",
            number_rooms=13
        )
        self.assertEqual(len(haunted_places), 2)

    def test_no_results(self):
        """Test when no spirits answer our call! 👻"""
        # Try to find non-existent user
        ghost = User.get_by_attr(
            username="NoGhost",
            city="RealWorld"
        )
        self.assertIsNone(ghost)

        # Try to find multiple non-existent places
        no_places = Place.get_by_attr(
            multiple=True,
            city="Heaven",
            number_rooms=777
        )
        self.assertEqual(len(no_places), 0)

    def test_mixed_attributes(self):
        """Test with a mix of valid and non-existent attributes! 🎃"""
        # This should work (existing attributes)
        place = Place.get_by_attr(
            city="Transylvania",
            number_rooms=13
        )
        self.assertIsNotNone(place)

        # This should return None (non-existent attribute)
        place = Place.get_by_attr(
            city="Transylvania",
            ghost_count=100  # This attribute doesn't exist
        )
        self.assertIsNone(place)

    def tearDown(self):
        """Clean up our haunted mess! 🧹"""
        User.repository._storage.clear()
        Place.repository._storage.clear()
        Review.repository._storage.clear()
        Amenity.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()