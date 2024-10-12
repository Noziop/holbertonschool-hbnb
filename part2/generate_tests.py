import os
import inspect

def generate_test_file(model_name, model_class):
    test_file_content = f"""
import unittest
from app.models.{model_name.lower()} import {model_name}

class Test{model_name}(unittest.TestCase):

    def setUp(self):
        self.{model_name.lower()} = {model_name}(**{{}})  # Add necessary parameters here

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
    with open(f"tests/test_{model_name.lower()}.py", "w") as f:
        f.write(test_file_content)

# Main script
models_dir = "app/models"
for filename in os.listdir(models_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        model_name = filename[:-3].capitalize()
        module = __import__(f"app.models.{filename[:-3]}", fromlist=[model_name])
        model_class = getattr(module, model_name)
        generate_test_file(model_name, model_class)

print("Test files generated successfully!")