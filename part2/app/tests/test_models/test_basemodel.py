import unittest
from datetime import datetime, timezone
import uuid
from app.models.basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        BaseModel.repository = self.repository
        self.basemodel = BaseModel()
        self.repository.add(self.basemodel)

    def tearDown(self):
        BaseModel.repository = InMemoryRepository()

    def test_create(self):
        new_basemodel = BaseModel.create(test_attr='test_value')
        self.assertIsInstance(new_basemodel, BaseModel)
        self.assertIn(new_basemodel.id, self.repository._storage)
        self.assertEqual(new_basemodel.test_attr, 'test_value')

    def test_get_by_id(self):
        retrieved_basemodel = BaseModel.get_by_id(self.basemodel.id)
        self.assertEqual(retrieved_basemodel.id, self.basemodel.id)

        with self.assertRaises(ValueError):
            BaseModel.get_by_id(str(uuid.uuid4()))

    def test_update(self):
        # Test updating an existing attribute
        original_updated_at = self.basemodel.updated_at
        self.basemodel.update({'updated_at': datetime.now(timezone.utc)})
        self.assertNotEqual(self.basemodel.updated_at, original_updated_at)

        # Test that we can't update 'id'
        with self.assertRaisesRegex(ValueError, "Cannot update id attribute"):
            self.basemodel.update({'id': 'new_id'})

        # Test that we can't update 'created_at'
        with self.assertRaisesRegex(ValueError, "Cannot update created_at attribute"):
            self.basemodel.update({'created_at': datetime.now(timezone.utc)})

        # Test that we can't add a new attribute
        with self.assertRaisesRegex(ValueError, "Invalid attribute: new_attr"):
            self.basemodel.update({'new_attr': 'new_value'})

    def test_delete(self):
        self.basemodel.delete()
        self.assertNotIn(self.basemodel.id, self.repository._storage)

        with self.assertRaises(ValueError):
            self.basemodel.delete()  # Trying to delete again should raise an error

    def test_to_dict(self):
        basemodel_dict = self.basemodel.to_dict()
        self.assertIsInstance(basemodel_dict, dict)
        self.assertIn('id', basemodel_dict)
        self.assertIn('created_at', basemodel_dict)
        self.assertIn('updated_at', basemodel_dict)

    def test_save(self):
        original_updated_at = self.basemodel.updated_at
        self.basemodel.save()
        self.assertNotEqual(self.basemodel.updated_at, original_updated_at)

    def test_init_with_kwargs(self):
        test_data = {
            'test_attr': 'test_value',
            'created_at': '2023-01-01T00:00:00',
            'updated_at': '2023-01-01T00:00:00'
        }
        model = BaseModel(**test_data)
        self.assertEqual(model.test_attr, 'test_value')
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_update_with_non_dict(self):
        with self.assertRaises(ValueError):
            self.basemodel.update("Not a dictionary")

    def test_save_exception(self):
        # Simuler une erreur dans le repository
        def mock_update(*args):
            raise Exception("Simulated error")
        
        self.basemodel.repository.update = mock_update
        
        with self.assertRaises(ValueError) as context:
            self.basemodel.save()
        
        self.assertTrue("Failed to save: Simulated error" in str(context.exception))

if __name__ == '__main__':
    unittest.main()