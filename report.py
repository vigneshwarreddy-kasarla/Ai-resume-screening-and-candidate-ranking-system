from jinja2 import Template
import datetime

template = """
<html>
<head><title>Screening Report</title></head>
<body>
<h1>AI Resume Screening Report</h1>
<p>Date: {{ date }}</p>

{% for score, name in results %}
<div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
<strong>{{ name }}</strong> — Score: {{ "%.3f"|format(score) }}
</div>
{% endfor %}
</body>
</html>
"""

def generate_report(results, filename="report.html"):
    html = Template(template).render(results=results, date=datetime.date.today())
    with open(filename, "w") as f:
        f.write(html)
    return filename
