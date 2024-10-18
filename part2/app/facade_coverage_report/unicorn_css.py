def get_unicorn_css():
    return """
    :root {{
        --unicorn-bg: linear-gradient(45deg, #ff9a9e 0%, #fad0c4 99%, #fad0c4 100%);
        --unicorn-text: #6a0dad;
        --unicorn-container: rgba(255, 255, 255, 0.8);
        --unicorn-covered: #ff69b4;
        --unicorn-not-covered: #ff4500;
        --unicorn-inherited: #9370db;
        --unicorn-facade: #00ced1;
        --unicorn-shadow: 0 0 20px rgba(255, 105, 180, 0.7);
    }}

    body.unicorn-mode {{
        background: var(--unicorn-bg);
        color: var(--unicorn-text);
        font-family: 'Comic Sans MS', cursive, sans-serif;
    }}

    body.unicorn-mode .container {{
        background-color: var(--unicorn-container);
        border-radius: 30px;
        box-shadow: var(--unicorn-shadow);
    }}

    body.unicorn-mode h1, body.unicorn-mode h2 {{
        text-shadow: 2px 2px 4px rgba(255, 105, 180, 0.5);
    }}

    body.unicorn-mode h1::before,
    body.unicorn-mode h1::after {{
        content: "🦄";
        margin: 0 10px;
    }}

    body.unicorn-mode .covered {{ 
        background-color: var(--unicorn-covered);
        border: 2px solid #ff1493;
    }}

    body.unicorn-mode .not-covered {{ 
        background-color: var(--unicorn-not-covered);
        border: 2px solid #ff6347;
    }}

    body.unicorn-mode .inherited {{ 
        background-color: var(--unicorn-inherited);
        border: 2px solid #8a2be2;
    }}

    body.unicorn-mode .facade-specific {{ 
        background-color: var(--unicorn-facade);
        border: 2px solid #40e0d0;
    }}

    body.unicorn-mode li {{
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
    }}

    body.unicorn-mode li:hover {{
        transform: scale(1.05) rotate(2deg);
    }}

    body.unicorn-mode .filter-btn {{
        background-color: #ff69b4;
        color: white;
        border: 2px solid #ff1493;
        font-weight: bold;
    }}

    body.unicorn-mode .filter-btn:hover {{
        background-color: #ff1493;
        transform: scale(1.1) rotate(-5deg);
    }}

    body.unicorn-mode .switch {{
        background-color: #ff69b4;
    }}

    body.unicorn-mode .slider:before {{
        background-color: #fff0f5;
    }}

    body.unicorn-mode input:checked + .slider {{
        background-color: #9370db;
    }}

    body.unicorn-mode #graph-container {{
        border: 3px solid #ff69b4;
        border-radius: 15px;
        overflow: hidden;
    }}

    body.unicorn-mode #tutorial {{
        background-color: rgba(255, 192, 203, 0.9);
        border: 3px solid #ff69b4;
    }}

    @keyframes sparkle {{
        0% {{ transform: scale(1); }}
        50% {{ transform: scale(1.2); }}
        100% {{ transform: scale(1); }}
    }}

    body.unicorn-mode .emoji {{
        display: inline-block;
        animation: sparkle 1s infinite;
    }}
    """
