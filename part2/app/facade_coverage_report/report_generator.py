import inspect
from bs4 import BeautifulSoup
from app.models import user, place, review, amenity, placeamenity, basemodel
from app.services.facade import HBnBFacade
import ast
import sys

def get_all_methods(cls):
    methods = set()
    for name, member in inspect.getmembers(cls):
        if inspect.isfunction(member) or inspect.ismethod(member):
            methods.add(name)
        elif isinstance(member, classmethod) or isinstance(member, staticmethod):
            methods.add(name)
    return methods

def get_inherited_methods(cls):
    base_methods = set()
    for base in cls.__bases__:
        base_methods.update(get_all_methods(base))
    return base_methods

def is_method_in_facade(model_name, method_name, facade_methods):
    for facade_method in facade_methods:
        if (model_name.lower() in facade_method.lower() and method_name.lower() in facade_method.lower()) or \
           facade_method.lower() == f"{model_name.lower()}_{method_name.lower()}":
            return True
    return False

def analyze_facade_methods(facade_class, model_classes):
    facade_methods = {}
    model_call_counts = {model: 0 for model in model_classes}
    total_calls = 0
    
    for name, method in inspect.getmembers(facade_class, predicate=inspect.ismethod):
        if name.startswith('__'):
            continue
        calls = analyze_method_calls(method, model_classes)
        facade_methods[name] = calls
        for model, _, _ in calls:
            model_call_counts[model] += 1
            total_calls += 1
    
    # Calculer les pourcentages
    model_percentages = {model: (count / total_calls * 100) if total_calls > 0 else 0 
                         for model, count in model_call_counts.items()}
    
    return facade_methods, model_percentages

def analyze_method_calls(method, model_classes):
    source = inspect.getsource(method)
    tree = ast.parse(source)
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                for model_name, model_class in model_classes.items():
                    if node.func.attr in dir(model_class):
                        call_type = 'direct' if node.func.attr in model_class.__dict__ else 'inherited'
                        calls.append((model_name, node.func.attr, call_type))
    return calls

def generate_report(facade_methods, model_percentages, coverage_data):
    report = ""
    for model_name, percentage in model_percentages.items():
        coverage = coverage_data.get(model_name, {}).get('coverage', 0)
        report += f"""
        <h2>{model_name}</h2>
        <div class="coverage-bar">
            <div class="coverage-progress" style="width: {coverage}%;"></div>
            <span class="coverage-text">{coverage:.2f}% covered</span>
        </div>
        <div class="usage-bar">
            <div class="usage-progress" style="width: {percentage}%;"></div>
            <span class="usage-text">{percentage:.2f}% of facade calls</span>
        </div>
        <ul>
        """
        model_class = getattr(sys.modules[__name__], model_name.lower())
        model_methods = get_all_methods(model_class)
        inherited_methods = get_inherited_methods(model_class)
        
        for method in model_methods:
            if method.startswith('_'):
                continue  # Skip private methods
            if method in inherited_methods and model_name != 'BaseModel':
                report += f"<li class='inherited'>{method} 🧙‍♀️</li>\n"
            elif is_method_in_facade(model_name, method, facade_methods):
                report += f"<li class='covered'>{method} 🦄</li>\n"
            else:
                if coverage_data.get(model_name, {}).get('missed_lines', 0) > 0:
                    report += f"<li class='not-covered'>{method} 💩 (Potentially unused)</li>\n"
                else:
                    report += f"<li class='not-covered'>{method} 💩</li>\n"
        
        report += "</ul>\n"
    
    report += "<h2>Facade-specific methods</h2>\n<ul>\n"
    for method, calls in facade_methods.items():
        if not calls:
            report += f"<li class='facade-specific'>{method} 🦄</li>\n"
        else:
            report += f"<li class='facade-specific'>{method} 🦄 (Calls: {', '.join([f'{model}.{func}' for model, func, _ in calls])})</li>\n"
    report += "</ul>\n"
    
    return report