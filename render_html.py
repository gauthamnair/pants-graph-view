import json
from jinja2 import Template

with open('gsecrets/jout.json') as f:
    j = json.load(f)

template_str = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hierarchical Structure</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <style>
        /* You can add styles here if needed */
        details > details {
            padding-left: 20px;
        }
    </style>
</head>
<body>

{% macro render_node(node) %}
    <details>
        <summary>
            {{ (node.rule_short_name or node.key) | e }}
        </summary>
        {{ node.key | e }}
        <details>
            <summary>value</summary>
            {{ node.value | e }}
        </details>
        {% for child in node.get("neighbors", []) %}
            {{ render_node(child) }}
        {% endfor %}
    </details>
{% endmacro %}

{{ render_node(data) }}

</body>
</html>
'''

template = Template(template_str)
rendered_html = template.render(data=j)
with open('gsecrets/hout.html', 'w') as f:
    f.write(rendered_html)

