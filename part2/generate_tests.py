import os
import sys
import inspect
from faker import Faker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fake = Faker()

def generate_mock_data(param_name, model_class):
    if 'name' in param_name and model_class.__name__ == 'Amenity':
        return fake.word() + ' ' + fake.word()
    elif 'email' in param_name:
        return fake.email()
    elif 'username' in param_name:
        return fake.user_name()
    elif 'password' in param_name:
        return fake.password()
    elif 'number' in param_name:
        return fake.random_int(min=1, max=10)
    elif 'price' in param_name:
        return fake.pyfloat(positive=True, min_value=1, max_value=1000, right_digits=2)
    elif 'latitude' in param_name:
        return fake.latitude()
    elif 'longitude' in param_name:
        return fake.longitude()
    elif 'text' in param_name:
        # Try different argument names for compatibility
        try:
            return fake.text(max_nb_chars=100)
        except TypeError:
            try:
                return fake.text(max_chars=100)
            except TypeError:
                return fake.text()[:100]  # Fallback to slicing
    elif 'description' in param_name:
        # Similar approach for description
        try:
            return fake.text(max_nb_chars=500)
        except TypeError:
            try:
                return fake.text(max_chars=500)
            except TypeError:
                return fake.text()[:500]  # Fallback to slicing
    elif 'id' in param_name:
        return fake.uuid4()
    else:
        return fake.word()

def generate_test_file(model_name, model_class):
    init_params = inspect.signature(model_class.__init__).parameters
    mock_params = {
        param: generate_mock_data(param, model_class) for param in init_params 
        if param != 'self' and param != 'kwargs'
    }
    
    test_file_content = f"""
import unittest
from app.models.{model_name.lower()} import {model_class.__name__}
from app.persistence.repository import InMemoryRepository

class Test{model_class.__name__}(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryRepository()
        {model_class.__name__}.repository = self.repository
        self.valid_params = {mock_params}
        self.{model_name.lower()} = {model_class.__name__}(**self.valid_params)

    def tearDown(self):
        {model_class.__name__}.repository = InMemoryRepository()

    def test_attributes(self):
        attrs = {[attr for attr in dir(model_class) if not attr.startswith('__') and not callable(getattr(model_class, attr))]}
        for attr in attrs:
            self.assertTrue(hasattr(self.{model_name.lower()}, attr))

    def test_methods(self):
        methods = {[method for method in dir(model_class) if callable(getattr(model_class, method)) and not method.startswith('__')]}
        for method in methods:
            self.assertTrue(hasattr(self.{model_name.lower()}, method))

    def test_create(self):
        new_{model_name.lower()} = {model_class.__name__}.create(**self.valid_params)
        self.assertIsInstance(new_{model_name.lower()}, {model_class.__name__})
        self.assertIn(new_{model_name.lower()}.id, self.repository._storage)

    def test_get_by_id(self):
        {model_name.lower()} = {model_class.__name__}.get_by_id(self.{model_name.lower()}.id)
        self.assertEqual({model_name.lower()}.id, self.{model_name.lower()}.id)

    def test_update(self):
        update_data = {{
            'name': 'Updated Name' if hasattr(self.{model_name.lower()}, 'name') else None,
            'description': 'Updated Description' if hasattr(self.{model_name.lower()}, 'description') else None
        }}
        update_data = {{k: v for k, v in update_data.items() if v is not None}}
        self.{model_name.lower()}.update(update_data)
        for key, value in update_data.items():
            self.assertEqual(getattr(self.{model_name.lower()}, key), value)

    def test_to_dict(self):
        {model_name.lower()}_dict = self.{model_name.lower()}.to_dict()
        self.assertIsInstance({model_name.lower()}_dict, dict)
        self.assertIn('id', {model_name.lower()}_dict)
        self.assertIn('created_at', {model_name.lower()}_dict)
        self.assertIn('updated_at', {model_name.lower()}_dict)

    def test_create_with_invalid_params(self):
        invalid_params = self.valid_params.copy()
        invalid_params['non_existent_param'] = 'invalid'
        with self.assertRaises(TypeError):
            {model_class.__name__}(**invalid_params)

    def test_update_with_invalid_params(self):
        with self.assertRaises(ValueError):
            self.{model_name.lower()}.update({{'invalid_param': 'invalid_value'}})

    # Add more specific tests here based on the model

if __name__ == '__main__':
    unittest.main()
"""
    os.makedirs(os.path.dirname(f"app/tests/test_models/test_{model_name.lower()}.py"), exist_ok=True)
    with open(f"app/tests/test_models/test_{model_name.lower()}.py", "w") as f:
        f.write(test_file_content)

# Main script
models_dir = "app/models"
for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        model_name = filename[:-3]
        module = __import__(f"app.models.{model_name}", fromlist=[model_name.capitalize()])
        
        if model_name == "basemodel":
            class_name = "BaseModel"
        elif model_name == "placeamenity":
            class_name = "PlaceAmenity"
        else:
            class_name = model_name.capitalize()
        
        model_class = getattr(module, class_name)
        generate_test_file(model_name, model_class)

print("Test files generated successfully!")