from .css_styles import get_css_styles
from .unicorn_css import get_unicorn_css
from .js_script import get_js_script

def get_html_template():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HBnB Model-Facade Coverage Report</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
        {css_styles}
        {unicorn_css}
        </style>
    </head>
    <body class="unicorn-mode">
        <div class="container">
            <h1>🦄 HBnB Model-Facade Coverage Report 🦄</h1>
            <div class="filter-buttons">
                <button class="filter-btn" data-emoji="all">🌈 All</button>
                <button class="filter-btn" data-emoji="🦄">🦄 Couvert</button>
                <button class="filter-btn" data-emoji="💩">💩 Non couvert</button>
                <button class="filter-btn" data-emoji="🧙‍♀️">🧙‍♀️ Hérité</button>
            </div>
            <div class="switches-container">
                <div class="switch-wrapper">
                    <label class="switch">
                        <input type="checkbox" id="themeToggle">
                        <span class="slider"></span>
                    </label>
                    <span class="switch-label">Mode Nuit Étoilée</span>
                </div>
                <div class="switch-wrapper">
                    <label class="switch">
                        <input type="checkbox" id="godModeToggle">
                        <span class="slider"></span>
                    </label>
                    <span class="switch-label">God Mode</span>
                </div>
            </div>
            {content}
            <div id="graph-container"></div>
        </div>
        <div id="tutorial" class="hidden">
            <p>Bienvenue dans le monde magique des tests ! 🧙‍♀️✨</p>
            <p>Chaque cercle représente une méthode. Les licornes (🦄) sont les méthodes bien couvertes, les caca (💩) sont celles qui ont besoin d'amour, et les sorcières (🧙‍♀️) sont les méthodes héritées.</p>
            <button onclick="closeTutorial()">J'ai compris la magie !</button>
        </div>
        <script>
        {js_script}
        </script>
    </body>
    </html>
    """