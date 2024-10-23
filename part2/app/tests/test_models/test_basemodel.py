"""Test module for BaseModel class."""

import unittest
from datetime import datetime, timezone
from uuid import UUID
from app.models.basemodel import BaseModel


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel class."""

    def setUp(self):
        """Set up test cases."""
        self.test_data = {
            'name': 'test_name',
            'value': 42
        }
        self.model = BaseModel(**self.test_data)

    def test_initialization(self):
        """Test BaseModel initialization."""
        # Test basic initialization
        self.assertEqual(self.model.name, 'test_name')
        self.assertEqual(self.model.value, 42)

        # Test ID generation
        self.assertTrue(isinstance(self.model.id, str))
        try:
            UUID(self.model.id)
        except ValueError:
            self.fail("ID is not a valid UUID")

        # Test timestamps
        self.assertTrue(isinstance(self.model.created_at, datetime))
        self.assertTrue(isinstance(self.model.updated_at, datetime))
        self.assertEqual(self.model.created_at.tzinfo, timezone.utc)
        self.assertEqual(self.model.updated_at.tzinfo, timezone.utc)

    def test_retrieval_methods(self):
        """Test get methods."""
        # Save instance for testing
        BaseModel.repository.add(self.model)

        # Test get_by_id
        retrieved = BaseModel.get_by_id(self.model.id)
        self.assertEqual(retrieved.id, self.model.id)

        # Test get_by_attr
        retrieved = BaseModel.get_by_attr('name', 'test_name')
        self.assertEqual(retrieved.name, 'test_name')

        # Test get_all
        all_models = BaseModel.get_all()
        self.assertIn(self.model, all_models)

        # Test invalid id
        with self.assertRaises(ValueError):
            BaseModel.get_by_id('invalid_id')

    def test_crud_operations(self):
        """Test CRUD operations."""
        # Test create
        new_model = BaseModel.create(name='created_test')
        self.assertEqual(new_model.name, 'created_test')
        self.assertTrue(isinstance(new_model.id, str))

        # Test update
        update_data = {'name': 'updated_name'}
        self.model.update(update_data)
        self.assertEqual(self.model.name, 'updated_name')

        # Test invalid update
        with self.assertRaises(ValueError):
            self.model.update({'id': 'new_id'})

        # Test save
        self.model.name = 'saved_name'
        saved_model = self.model.save()
        self.assertEqual(saved_model.name, 'saved_name')

        # Test delete
        self.assertTrue(new_model.delete())
        with self.assertRaises(ValueError):
            BaseModel.get_by_id(new_model.id)

    def test_serialization(self):
        """Test serialization methods."""
        # Test to_dict
        data_dict = self.model.to_dict()
        
        # Check basic attributes
        self.assertEqual(data_dict['id'], self.model.id)
        self.assertTrue('created_at' in data_dict)
        self.assertTrue('updated_at' in data_dict)

        # Check datetime serialization
        try:
            datetime.fromisoformat(data_dict['created_at'])
            datetime.fromisoformat(data_dict['updated_at'])
        except ValueError:
            self.fail("Datetime not properly serialized")

    def test_validation(self):
        """Test input validation."""
        # Test invalid attribute
        with self.assertRaises(ValueError):
            self.model.update({'invalid_attr': 'value'})

        # Test protected attributes
        with self.assertRaises(ValueError):
            self.model.update({'created_at': datetime.now()})

    def tearDown(self):
        """Clean up after tests."""
        # Clear repository
        BaseModel.repository._storage.clear()


if __name__ == '__main__':
    unittest.main()