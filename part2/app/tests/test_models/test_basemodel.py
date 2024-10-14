import unittest
import uuid
from datetime import datetime, timezone
from app.models.basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        BaseModel.repository = self.repository
        self.valid_params = {}
        self.basemodel = BaseModel(**self.valid_params)
        self.repository.add(self.basemodel)

    def tearDown(self):
        BaseModel.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['id', 'created_at', 'updated_at']
        for attr in attrs:
            self.assertTrue(hasattr(self.basemodel, attr))

    def test_methods(self):
        methods = ['create', 'get_by_id', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(BaseModel, method) if method in ['create', 'get_by_id'] else hasattr(self.basemodel, method))

    def test_create(self):
        new_basemodel = BaseModel.create(**self.valid_params)
        self.assertIsInstance(new_basemodel, BaseModel)
        self.assertIn(new_basemodel.id, self.repository._storage)

    def test_get_by_id(self):
        retrieved_basemodel = BaseModel.get_by_id(self.basemodel.id)
        self.assertIsNotNone(retrieved_basemodel)
        self.assertEqual(retrieved_basemodel.id, self.basemodel.id)

        non_existent_id = str(uuid.uuid4())
        self.assertIsNone(BaseModel.get_by_id(non_existent_id))

    def test_update(self):
        original_updated_at = self.basemodel.updated_at
        self.basemodel.update({'updated_at': datetime.now(timezone.utc)})
        self.assertNotEqual(self.basemodel.updated_at, original_updated_at)

        # Test that id and created_at cannot be updated
        original_id = self.basemodel.id
        original_created_at = self.basemodel.created_at
        self.basemodel.update({'id': 'new_id', 'created_at': datetime.now(timezone.utc)})
        self.assertEqual(self.basemodel.id, original_id)
        self.assertEqual(self.basemodel.created_at, original_created_at)

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

    def test_update_with_invalid_params(self):
        with self.assertRaises(AttributeError):
            self.basemodel.update({'invalid_param': 'invalid_value'})

if __name__ == '__main__':
    unittest.main()