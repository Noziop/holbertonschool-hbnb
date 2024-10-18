def get_js_script():
    return """
    // Filtrage
    document.querySelectorAll('.filter-btn').forEach(btn => {{
        btn.addEventListener('click', () => {{
            const emoji = btn.dataset.emoji;
            document.querySelectorAll('li').forEach(li => {{
                if (emoji === 'all') {{
                    li.style.display = 'block';
                }} else {{
                    li.style.display = li.textContent.includes(emoji) ? 'block' : 'none';
                }}
            }});
        }});
    }});

    // God Mode
    document.getElementById('godModeToggle').addEventListener('change', (e) => {{
        const isGodMode = e.target.checked;
        document.querySelectorAll('.method-info').forEach(span => {{
            span.contentEditable = isGodMode;
        }});
    }});

    // Theme Toggle
    document.getElementById('modeToggle').addEventListener('change', (e) => {{
        document.body.classList.toggle('dark-mode');
        document.body.classList.toggle('light-mode');
    }});

    // Unicorn Mode Toggle
    document.getElementById('unicornModeToggle').addEventListener('change', (e) => {{
        document.body.classList.toggle('unicorn-mode');
    }});

    // Tutoriel
    function closeTutorial() {{
        document.getElementById('tutorial').classList.add('hidden');
    }}

    // D3.js visualization
    const data = [
        {{name: "Covered", value: document.querySelectorAll('.covered').length}},
        {{name: "Not Covered", value: document.querySelectorAll('.not-covered').length}},
        {{name: "Inherited", value: document.querySelectorAll('.inherited').length}}
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
        .attr("transform", `translate(${{width / 2}},${{height / 2}})`);

    svg.selectAll("path")
        .data(pie(data))
        .enter()
        .append("path")
        .attr("d", arc)
        .attr("fill", d => color(d.data.name));
    """