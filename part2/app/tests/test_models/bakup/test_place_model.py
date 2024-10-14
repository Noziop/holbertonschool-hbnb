import unittest
from models.place import Place
from persistence.repository import InMemoryRepository

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()

    def test_create_place(self):
        place = Place(
            name="Eiffel Tower",
            description="Iconic landmark in Paris",
            number_rooms=1,
            number_bathrooms=1,
            max_guest=10,
            price_by_night=100,
            latitude=48.8584,
            longitude=2.2945,
            city="Paris",
            country="France",
            owner_id="user123"
        )
        self.repo.add(place)
        self.assertIsNotNone(place.id)
        self.assertEqual(place.name, "Eiffel Tower")
        self.assertEqual(place.city, "Paris")
        self.assertEqual(place.country, "France")
        self.assertEqual(place.owner_id, "user123")

    def test_get_place(self):
        place = Place(
            name="Louvre",
            description="World's largest art museum",
            number_rooms=1,
            number_bathrooms=1,
            max_guest=100,
            price_by_night=0,
            latitude=48.8606,
            longitude=2.3376,
            city="Paris",
            country="France",
            owner_id="user456"
        )
        self.repo.add(place)
        retrieved_place = self.repo.get(place.id)
        self.assertEqual(retrieved_place.name, "Louvre")
        self.assertEqual(retrieved_place.city, "Paris")

    def test_update_place(self):
        place = Place(
            name="Arc de Triomphe",
            description="Iconic monument",
            number_rooms=0,
            number_bathrooms=0,
            max_guest=0,
            price_by_night=0,
            latitude=48.8738,
            longitude=2.2950,
            city="Paris",
            country="France",
            owner_id="user789"
        )
        self.repo.add(place)
        self.repo.update(place.id, {"name": "Updated Arc de Triomphe", "max_guest": 10})
        updated_place = self.repo.get(place.id)
        self.assertEqual(updated_place.name, "Updated Arc de Triomphe")
        self.assertEqual(updated_place.max_guest, 10)

    def test_delete_place(self):
        place = Place(
            name="Notre-Dame",
            description="Medieval Catholic cathedral",
            number_rooms=0,
            number_bathrooms=0,
            max_guest=0,
            price_by_night=0,
            latitude=48.8530,
            longitude=2.3499,
            city="Paris",
            country="France",
            owner_id="user101"
        )
        self.repo.add(place)
        self.repo.delete(place.id)
        self.assertIsNone(self.repo.get(place.id))

if __name__ == '__main__':
    unittest.main()