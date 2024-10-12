import os
import inspect
import sys

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def generate_test_file(model_name, model_class):
    test_file_content = f"""
import unittest
from app.models.{model_name.lower()} import {model_name}

class Test{model_name}(unittest.TestCase):

    def setUp(self):
        self.{model_name.lower()} = {model_name}()  # Remove parameters for now

    def test_attributes(self):
        # Test that all attributes are present
        attrs = {inspect.getmembers(model_class, lambda a: not inspect.isroutine(a))}
        for attr in attrs:
            self.assertTrue(hasattr(self.{model_name.lower()}, attr[0]))

    def test_methods(self):
        # Test that all methods are present
        methods = {inspect.getmembers(model_class, predicate=inspect.ismethod)}
        for method in methods:
            self.assertTrue(hasattr(self.{model_name.lower()}, method[0]))

    def test_to_dict(self):
        # Test the to_dict method
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
        model_name = ''.join(word.capitalize() for word in filename[:-3].split('_'))
        module = __import__(f"app.models.{filename[:-3]}", fromlist=[model_name])
        model_class = getattr(module, model_name)
        generate_test_file(model_name, model_class)

print("Test files generated successfully!")