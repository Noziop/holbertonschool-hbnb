import unittest
from app.models.placeamenity import PlaceAmenity
from app.persistence.repository import InMemoryRepository
from app.models.place import Place
from app.models.amenity import Amenity

class TestPlaceAmenity(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        PlaceAmenity.repository = self.repository
        self.place = Place.create(name="Test Place", description="Test Description", number_rooms=2, number_bathrooms=1, max_guest=4, price_by_night=100, latitude=45.5, longitude=-73.5, owner_id="test_owner")
        self.amenity = Amenity.create(name="Test Amenity")
        self.valid_params = {
            'place_id': self.place.id,
            'amenity_id': self.amenity.id
        }
        self.place_amenity = PlaceAmenity.create(**self.valid_params)

    def tearDown(self):
        PlaceAmenity.repository = InMemoryRepository()

    def test_create(self):
        new_place_amenity = PlaceAmenity.create(**self.valid_params)
        self.assertIsInstance(new_place_amenity, PlaceAmenity)
        self.assertIn(new_place_amenity.id, self.repository._storage)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['place_id'] = ''
        with self.assertRaises(ValueError):
            PlaceAmenity.create(**invalid_params)

    def test_get_by_place(self):
        results = PlaceAmenity.get_by_place(self.place.id)
        self.assertIn(self.place_amenity, results)

    def test_get_by_amenity(self):
        results = PlaceAmenity.get_by_amenity(self.amenity.id)
        self.assertIn(self.place_amenity, results)

    def test_get_places(self):
        places = PlaceAmenity.get_places(self.amenity.id)
        self.assertIn(self.place, places)

    def test_update(self):
        new_place = Place.create(name="New Place", description="New Description", number_rooms=1, number_bathrooms=1, max_guest=2, price_by_night=50, latitude=40.7, longitude=-74.0, owner_id="new_owner")
        update_data = {'place_id': new_place.id}
        self.place_amenity.update(update_data)
        self.assertEqual(self.place_amenity.place_id, new_place.id)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.place_amenity.update({'invalid_param': 'invalid_value'})

    def test_to_dict(self):
        place_amenity_dict = self.place_amenity.to_dict()
        self.assertIsInstance(place_amenity_dict, dict)
        self.assertIn('id', place_amenity_dict)
        self.assertIn('place_id', place_amenity_dict)
        self.assertIn('amenity_id', place_amenity_dict)
        self.assertIn('created_at', place_amenity_dict)
        self.assertIn('updated_at', place_amenity_dict)

if __name__ == '__main__':
    unittest.main()