def get_css_styles():
    return """
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
    """
