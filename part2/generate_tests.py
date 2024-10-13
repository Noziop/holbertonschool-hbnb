import os
import sys
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_test_file(model_name, model_class):
    # Get the required parameters for the constructor
    init_params = inspect.signature(model_class.__init__).parameters
    mock_params = {
        param: f"test_{param}" for param in init_params 
        if param != 'self' and param != 'kwargs'
    }
    
    test_file_content = f"""
import unittest
from app.models.{model_name.lower()} import {model_name.capitalize()}

class Test{model_name.capitalize()}(unittest.TestCase):

    def setUp(self):
        self.{model_name.lower()} = {model_name.capitalize()}(**{mock_params})

    def test_attributes(self):
        attrs = {[attr for attr in dir(model_class) if not attr.startswith('__') and not callable(getattr(model_class, attr))]}
        for attr in attrs:
            self.assertTrue(hasattr(self.{model_name.lower()}, attr))

    def test_methods(self):
        methods = {[method for method in dir(model_class) if callable(getattr(model_class, method)) and not method.startswith('__')]}
        for method in methods:
            self.assertTrue(hasattr(self.{model_name.lower()}, method))

    def test_to_dict(self):
        model_dict = self.{model_name.lower()}.to_dict()
        self.assertIsInstance(model_dict, dict)
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)

    # Add more specific tests here

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