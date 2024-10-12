import unittest
from models.place import Place
from persistence.repository import InMemoryRepository

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.repo = InMemoryRepository()

    def test_create_place(self):
        place = Place(name="Eiffel Tower", city="Paris", country="France", owner_id="user123")
        self.repo.add(place)
        self.assertIsNotNone(place.id)
        self.assertEqual(place.name, "Eiffel Tower")

    def test_get_place(self):
        place = Place(name="Louvre", city="Paris", country="France", owner_id="user456")
        self.repo.add(place)
        retrieved_place = self.repo.get(place.id)
        self.assertEqual(retrieved_place.name, "Louvre")

    def test_update_place(self):
        place = Place(name="Arc de Triomphe", city="Paris", country="France", owner_id="user789")
        self.repo.add(place)
        self.repo.update(place.id, {"name": "Updated Arc de Triomphe"})
        updated_place = self.repo.get(place.id)
        self.assertEqual(updated_place.name, "Updated Arc de Triomphe")

    def test_delete_place(self):
        place = Place(name="Notre-Dame", city="Paris", country="France", owner_id="user101")
        self.repo.add(place)
        self.repo.delete(place.id)
        self.assertIsNone(self.repo.get(place.id))

if __name__ == '__main__':
    unittest.main()