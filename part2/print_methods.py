import os
import inspect
import importlib.util

def get_methods_from_file(file_path):
    spec = importlib.util.spec_from_file_location("module", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    methods = {}
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj):
            class_methods = [method for method in inspect.getmembers(obj, predicate=inspect.isfunction) if not method[0].startswith('_')]
            methods[obj.__name__] = [method[0] for method in class_methods]
    
    return methods

def get_methods_in_directory(directory):
    all_methods = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                file_path = os.path.join(root, file)
                try:
                    methods = get_methods_from_file(file_path)
                    all_methods[file] = methods
                except Exception as e:
                    print(f"Error processing file {file}: {str(e)}")
    return all_methods

def get_all_methods():
    service_dir = "app/services"
    model_dir = "app/models"

    service_methods = get_methods_in_directory(service_dir)
    model_methods = get_methods_in_directory(model_dir)

    return {"services": service_methods, "models": model_methods}

if __name__ == "__main__":
    methods = get_all_methods()
    print(methods)