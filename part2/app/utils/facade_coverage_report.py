import inspect
import os
import subprocess
import time
from bs4 import BeautifulSoup
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
    
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HBnB Model-Facade Coverage Report</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            :root {{
                --bg-light: #f4f4f4;
                --text-light: #333;
                --container-light: #fff;
                --covered-light: #98FB98;
                --not-covered-light: #FFA07A;
                --inherited-light: #D3D3D3;
                --facade-specific-light: #87CEFA;
                
                --bg-dark: #1a1a1a;
                --text-dark: #f4f4f4;
                --container-dark: #2c3e50;
                --covered-dark: #2ecc71;
                --not-covered-dark: #e74c3c;
                --inherited-dark: #7f8c8d;
                --facade-specific-dark: #4682B4;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                transition: all 0.3s ease;
            }}
            .container {{
                max-width: 800px;
                margin: auto;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }}
            h1, h2 {{
                text-align: center;
                margin-bottom: 20px;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin-bottom: 10px;
                padding: 12px;
                border-radius: 8px;
                transition: all 0.3s ease;
            }}
            li:hover {{
                transform: translateX(5px);
            }}
            .covered {{ background-color: var(--covered-light); }}
            .not-covered {{ background-color: var(--not-covered-light); }}
            .inherited {{ background-color: var(--inherited-light); }}
            .facade-specific {{ background-color: var(--facade-specific-light); }}
            
            body.light-mode {{
                background-color: var(--bg-light);
                color: var(--text-light);
            }}
            body.light-mode .container {{
                background-color: var(--container-light);
            }}
            
            body.dark-mode {{
                background-color: var(--bg-dark);
                color: var(--text-dark);
            }}
            body.dark-mode .container {{
                background-color: var(--container-dark);
            }}
            body.dark-mode .covered {{ background-color: var(--covered-dark); }}
            body.dark-mode .not-covered {{ background-color: var(--not-covered-dark); }}
            body.dark-mode .inherited {{ background-color: var(--inherited-dark); }}
            body.dark-mode .facade-specific {{ background-color: var(--facade-specific-dark); }}
            
            .switch {{
                position: relative;
                display: inline-block;
                width: 60px;
                height: 34px;
                margin-bottom: 20px;
            }}
            .switch input {{
                opacity: 0;
                width: 0;
                height: 0;
            }}
            .slider {{
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: #ccc;
                transition: .4s;
                border-radius: 34px;
            }}
            .slider:before {{
                position: absolute;
                content: "";
                height: 26px;
                width: 26px;
                left: 4px;
                bottom: 4px;
                background-color: white;
                transition: .4s;
                border-radius: 50%;
            }}
            input:checked + .slider {{
                background-color: #ff69b4;
            }}
            input:checked + .slider:before {{
                transform: translateX(26px);
            }}
            
            body.unicorn-mode {{
                background-image: linear-gradient(to right, violet, indigo, blue, green, yellow, orange, red);
                color: white;
            }}
            body.unicorn-mode .container {{
                background-color: rgba(255, 255, 255, 0.8);
                color: #333;
            }}
            body.unicorn-mode h1::before,
            body.unicorn-mode h1::after {{
                content: "🦄";
                margin: 0 10px;
            }}
            .filter-buttons {{
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }}
            .filter-btn {{
                margin: 0 10px;
                padding: 10px 15px;
                border: none;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            .filter-btn:hover {{
                transform: scale(1.1);
            }}
            .method-name {{
                font-weight: bold;
                margin-right: 10px;
            }}
            .method-info {{
                font-style: italic;
                color: #666;
            }}
            #graph-container {{
                width: 100%;
                height: 500px;
                border: 1px solid #ddd;
                margin-top: 20px;
            }}
            #tutorial {{
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 10px;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 1000;
                box-shadow: 0 0 10px rgba(0,0,0,0.3);
            }}
            .hidden {{ display: none; }}
        </style>
    </head>
    <body class="light-mode">
        <div class="container">
            <h1>HBnB Model-Facade Coverage Report</h1>
            <div class="filter-buttons">
                <button class="filter-btn" data-emoji="🦄">🦄 Couvert</button>
                <button class="filter-btn" data-emoji="💩">💩 Non couvert</button>
                <button class="filter-btn" data-emoji="🧙‍♀️">🧙‍♀️ Hérité</button>
            </div>
            <label class="switch">
                <input type="checkbox" id="modeToggle">
                <span class="slider"></span>
                Theme
            </label>
            <label class="switch">
                <input type="checkbox" id="godModeToggle">
                <span class="slider"></span>
                God Mode
            </label>
            {content}
            <div id="graph-container"></div>
        </div>
        <div id="tutorial" class="hidden">
            <p>Bienvenue dans le monde magique des tests ! 🧙‍♀️✨</p>
            <p>Chaque cercle représente une méthode. Les licornes (🦄) sont les méthodes bien couvertes, les caca (💩) sont celles qui ont besoin d'amour, et les sorcières (🧙‍♀️) sont les méthodes héritées.</p>
            <button onclick="closeTutorial()">J'ai compris la magie !</button>
        </div>
        <script>
            // ... (code JavaScript précédent) ...
            
            // Filtrage
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.addEventListener('click', () => {
                    const emoji = btn.dataset.emoji;
                    document.querySelectorAll('li').forEach(li => {
                        li.style.display = li.textContent.includes(emoji) ? 'block' : 'none';
                    });
                });
            });

            // God Mode
            document.getElementById('godModeToggle').addEventListener('change', (e) => {
                const isGodMode = e.target.checked;
                document.querySelectorAll('.method-info').forEach(span => {
                    span.contentEditable = isGodMode;
                });
            });

            // Tutoriel
            function closeTutorial() {
                document.getElementById('tutorial').classList.add('hidden');
            }

            // D3.js visualization (basic example)
            const data = [
                {name: "Covered", value: document.querySelectorAll('.covered').length},
                {name: "Not Covered", value: document.querySelectorAll('.not-covered').length},
                {name: "Inherited", value: document.querySelectorAll('.inherited').length}
            ];

            const width = 500;
            const height = 500;
            const radius = Math.min(width, height) / 2;

            const color = d3.scaleOrdinal()
                .domain(["Covered", "Not Covered", "Inherited"])
                .range(["#98FB98", "#FFA07A", "#D3D3D3"]);

            const pie = d3.pie()
                .value(d => d.value);

            const arc = d3.arc()
                .innerRadius(0)
                .outerRadius(radius);

            const svg = d3.select("#graph-container")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${width / 2},${height / 2})`);

            svg.selectAll("path")
                .data(pie(data))
                .enter()
                .append("path")
                .attr("d", arc)
                .attr("fill", d => color(d.data.name));
        </script>
    </body>
    </html>
    """
    
    with open(os.path.join(output_dir, 'model_facade_coverage_report.html'), 'w') as f:
        f.write(html_template.format(content=content))

if __name__ == "__main__":
    run_coverage()
    output_dir = "facade_coverage_report"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    generate_html_report(output_dir)
    print(f"Report generated in {output_dir}")