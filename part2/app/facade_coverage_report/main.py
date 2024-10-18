import os
import subprocess
import time
import inspect
from bs4 import BeautifulSoup
from .html_template import get_html_template
from .css_styles import get_css_styles
from .unicorn_css import get_unicorn_css
from .js_script import get_js_script
from app.models import user, place, review, amenity, placeamenity, basemodel
from app.services.facade import HBnBFacade

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

def run_coverage():
    subprocess.run(["coverage", "run", "--rcfile=../.coveragerc", "-m", "unittest", "discover", "app/"])
    time.sleep(20)  # Attendre 20 secondes
    subprocess.run(["coverage", "html", "--rcfile=../.coveragerc"])

def parse_coverage_report():
    with open('htmlcov/index.html', 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    coverage_data = {}
    for row in soup.find_all('tr', class_='file'):
        filename = row.find('a').text
        if 'models' in filename:
            model_name = filename.split('/')[-1].split('.')[0]
            coverage_data[model_name] = {}
            missed_lines = row.find('td', class_='right').text
            coverage_data[model_name]['missed_lines'] = int(missed_lines)
    
    return coverage_data

def generate_report():
    models = {
        'User': user.User,
        'Place': place.Place,
        'Review': review.Review,
        'Amenity': amenity.Amenity,
        'PlaceAmenity': placeamenity.PlaceAmenity,
        'BaseModel': basemodel.BaseModel
    }
    
    facade = HBnBFacade()
    facade_methods = get_all_methods(HBnBFacade)
    
    coverage_data = parse_coverage_report()
    
    report = ""
    
    for model_name, model_class in models.items():
        report += f"<h2>{model_name}</h2>\n<ul>\n"
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
    for method in facade_methods:
        if not any(is_method_in_facade(model_name, method, [method]) for model_name in models):
            report += f"<li class='facade-specific'>{method} 🦄</li>\n"
    report += "</ul>\n"
    
    return report

def generate_html_report(output_dir):
    content = generate_report()
    html_template = get_html_template()
    css_styles = get_css_styles()
    unicorn_css = get_unicorn_css()
    js_script = get_js_script()
    
    with open(os.path.join(output_dir, 'model_facade_coverage_report.html'), 'w') as f:
        f.write(html_template.format(
            content=content,
            css_styles=css_styles,
            unicorn_css=unicorn_css,
            js_script=js_script
        ))

def main():
    run_coverage()
    output_dir = "facade_coverage_report"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generate_html_report(output_dir)
    print(f"Report generated in {output_dir}")

if __name__ == "__main__":
    main()