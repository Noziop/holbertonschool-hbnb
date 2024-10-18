import subprocess
import time
import os
from datetime import datetime
from bs4 import BeautifulSoup

def get_latest_modification_time(directory):
    latest_time = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                mod_time = os.path.getmtime(file_path)
                if mod_time > latest_time:
                    latest_time = mod_time
    return latest_time

def check_existing_coverage_report():
    coverage_report_path = 'htmlcov/index.html'
    if os.path.exists(coverage_report_path):
        report_time = os.path.getmtime(coverage_report_path)
        latest_code_time = get_latest_modification_time('app')
        return report_time > latest_code_time
    return False

def run_coverage(force=False):
    if force or not check_existing_coverage_report():
        print("Génération d'un nouveau rapport de couverture... 🦄✨")
        subprocess.run(["coverage", "run", "--rcfile=../.coveragerc", "-m", "unittest", "discover", "app/"])
        subprocess.run(["coverage", "html", "--rcfile=../.coveragerc"])
        print("Nouveau rapport généré avec succès ! 🎉")
    else:
        print("Un rapport de couverture à jour existe déjà. Utilisation du rapport existant. 🌈")

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
            total_lines = row.find_all('td', class_='right')[1].text
            coverage_data[model_name]['total_lines'] = int(total_lines)
            coverage_data[model_name]['coverage'] = (int(total_lines) - int(missed_lines)) / int(total_lines) * 100
    
    return coverage_data

def generate_coverage_stats():
    coverage_data = parse_coverage_report()
    total_lines = sum(data['total_lines'] for data in coverage_data.values())
    total_covered = sum(data['total_lines'] - data['missed_lines'] for data in coverage_data.values())
    overall_coverage = (total_covered / total_lines) * 100 if total_lines > 0 else 0

    stats = {
        'overall_coverage': overall_coverage,
        'models': coverage_data
    }
    return stats

if __name__ == "__main__":
    run_coverage()
    stats = generate_coverage_stats()
    print(f"Couverture globale : {stats['overall_coverage']:.2f}%")
    for model, data in stats['models'].items():
        print(f"{model}: {data['coverage']:.2f}%")