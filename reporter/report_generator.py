import json
import os
from datetime import datetime
from jinja2 import Template
from dotenv import load_dotenv

load_dotenv()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>QA Report — {{ timestamp }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e0e0e0; padding: 40px; }
        h1 { color: #ffffff; font-size: 28px; margin-bottom: 6px; }
        .subtitle { color: #888; font-size: 14px; margin-bottom: 40px; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
        .card { background: #1a1d27; border-radius: 12px; padding: 24px; border: 1px solid #2a2d3a; }
        .card .label { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px; }
        .card .value { font-size: 36px; font-weight: bold; margin-top: 8px; }
        .green { color: #4ade80; }
        .red { color: #f87171; }
        .blue { color: #60a5fa; }
        .yellow { color: #facc15; }
        .section { background: #1a1d27; border-radius: 12px; padding: 28px; margin-bottom: 24px; border: 1px solid #2a2d3a; }
        .section h2 { font-size: 16px; color: #aaa; margin-bottom: 20px; text-transform: uppercase; letter-spacing: 1px; }
        .test-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #2a2d3a; }
        .test-row:last-child { border-bottom: none; }
        .badge { padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: bold; }
        .badge-pass { background: #14532d; color: #4ade80; }
        .badge-fail { background: #7f1d1d; color: #f87171; }
        .failure-block { background: #1f0e0e; border-left: 3px solid #f87171; padding: 16px; border-radius: 6px; margin-top: 12px; }
        .failure-block pre { font-size: 12px; color: #fca5a5; white-space: pre-wrap; word-break: break-word; }
        .issue-link { color: #60a5fa; text-decoration: none; font-size: 13px; }
        .issue-link:hover { text-decoration: underline; }
        .footer { text-align: center; color: #444; font-size: 12px; margin-top: 40px; }
    </style>
</head>
<body>
    <h1>🤖 QA Agent Report</h1>
    <div class="subtitle">Generated: {{ timestamp }} &nbsp;|&nbsp; Run by: QA Agent Phase 1</div>

    <div class="grid">
        <div class="card">
            <div class="label">Total Tests</div>
            <div class="value blue">{{ test_summary.total }}</div>
        </div>
        <div class="card">
            <div class="label">Passed</div>
            <div class="value green">{{ test_summary.passed }}</div>
        </div>
        <div class="card">
            <div class="label">Failed</div>
            <div class="value {% if test_summary.failed > 0 %}red{% else %}green{% endif %}">{{ test_summary.failed }}</div>
        </div>
        <div class="card">
            <div class="label">Coverage</div>
            <div class="value {% if test_summary.coverage_percent >= 80 %}green{% else %}yellow{% endif %}">{{ test_summary.coverage_percent }}%</div>
        </div>
    </div>

    <div class="section">
        <h2>API Test Results</h2>
        {% for result in api_summary.results %}
        <div class="test-row">
            <span>{{ result.description }}</span>
            <span style="color:#888; font-size:13px;">{{ result.method }} {{ result.response_time_ms }}ms</span>
            <span class="badge {% if result.passed %}badge-pass{% else %}badge-fail{% endif %}">
                {% if result.passed %}PASS{% else %}FAIL{% endif %}
            </span>
        </div>
        {% endfor %}
    </div>

    {% if test_summary.failures %}
    <div class="section">
        <h2>❌ Failures & Bugs</h2>
        {% for failure in test_summary.failures %}
        <div class="failure-block">
            <strong style="color:#f87171;">{{ failure.name }}</strong>
            <pre>{{ failure.message }}</pre>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    {% if github_issues %}
    <div class="section">
        <h2>🐛 GitHub Issues Created</h2>
        {% for url in github_issues %}
        <div class="test-row">
            <a href="{{ url }}" class="issue-link" target="_blank">{{ url }}</a>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="footer">QA Agent — agentalent.ai &nbsp;|&nbsp; Built by Devansh</div>
</body>
</html>
"""

def generate_report(test_summary, api_summary, github_issues=None, output_path="qa_report.html"):
    """Render the HTML report and save it."""
    
    template = Template(HTML_TEMPLATE)
    html = template.render(
        timestamp=test_summary.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        test_summary=test_summary,
        api_summary=api_summary,
        github_issues=github_issues or []
    )
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"\n✅ HTML report saved → {output_path}")
    return output_path


if __name__ == "__main__":
    # Test with dummy data
    dummy_test = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": 7, "passed": 7, "failed": 0,
        "coverage_percent": 100.0, "failures": []
    }
    dummy_api = {
        "total": 7, "passed": 7, "failed": 0,
        "results": [
            {"description": "Fetch single post", "method": "GET", "passed": True, "response_time_ms": 120},
            {"description": "Create a post",     "method": "POST","passed": True, "response_time_ms": 200},
        ]
    }
    generate_report(dummy_test, dummy_api, ["https://github.com/Devansh-Daga/qa-agent/issues/1"])