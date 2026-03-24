import json
from datetime import datetime

def generate(results, output_name):
    # JSON Report
    report_data = {
        "tool": "ShadowRecon",
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }

    with open(f"{output_name}.json", "w") as f:
        json.dump(report_data, f, indent=4)

    # HTML Report
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ShadowRecon Report</title>
    <style>
        body {{ font-family: monospace; background: #0d0d0d; color: #00ff00; padding: 20px; }}
        h1 {{ color: #ff4444; }}
        h2 {{ color: #00aaff; border-bottom: 1px solid #333; padding-bottom: 5px; }}
        .finding {{ background: #1a1a1a; border-left: 4px solid #00ff00; padding: 10px; margin: 10px 0; }}
        .vuln {{ border-left-color: #ff4444; }}
        .meta {{ color: #888; font-size: 0.85em; }}
        pre {{ background: #111; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>🔍 ShadowRecon Report</h1>
    <p class="meta">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | github.com/saksht</p>
    <hr>
"""

    for module, data in results.items():
        html += f"<h2>{module.upper()}</h2>"
        if not data:
            html += "<p>No findings.</p>"
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    html += f'<div class="finding vuln"><pre>{json.dumps(item, indent=2)}</pre></div>'
                else:
                    html += f'<div class="finding">{item}</div>'

    html += """
</body>
</html>"""

    with open(f"{output_name}.html", "w") as f:
        f.write(html)
