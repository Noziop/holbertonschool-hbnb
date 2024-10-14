
import unittest
from app.models.basemodel import BaseModel
from app.persistence.repository import InMemoryRepository

class TestBaseModel(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        BaseModel.repository = self.repository
        self.valid_params = {}
        self.basemodel = BaseModel(**self.valid_params)

    def tearDown(self):
        BaseModel.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = ['repository']
        for attr in attrs:
            self.assertTrue(hasattr(self.basemodel, attr))

    def test_methods(self):
        methods = ['create', 'get_by_id', 'save', 'to_dict', 'update']
        for method in methods:
            self.assertTrue(hasattr(self.basemodel, method))

    def test_create(self):
        new_basemodel = BaseModel.create(**self.valid_params)
        self.assertIsInstance(new_basemodel, BaseModel)
        self.assertIn(new_basemodel.id, self.repository._storage)

    def test_get_by_id(self):
        basemodel = BaseModel.get_by_id(self.basemodel.id)
        self.assertEqual(basemodel.id, self.basemodel.id)

    def test_update(self):
        update_data = {
            'name': 'Updated Name' if hasattr(self.basemodel, 'name') else None,
            'description': 'Updated Description' if hasattr(self.basemodel, 'description') else None
        }
        update_data = {k: v for k, v in update_data.items() if v is not None}
        self.basemodel.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.basemodel, key), value)

    def test_to_dict(self):
        basemodel_dict = self.basemodel.to_dict()
        self.assertIsInstance(basemodel_dict, dict)
        self.assertIn('id', basemodel_dict)
        self.assertIn('created_at', basemodel_dict)
        self.assertIn('updated_at', basemodel_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            BaseModel(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.basemodel.update({'invalid_param': 'invalid_value'})

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
