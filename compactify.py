from typing import cast

import pydot
import re


graphs = pydot.graph_from_dot_file('gsecrets/graph.003.dot')

graph = cast(pydot.Dot, graphs[0])


def compactify_qualname(x):
    parts = x.split('.')
    if len(parts) <= 1:
        return x

    return '.'.join([p[0] for p in parts[:-1]]) + '.\n' + parts[-1]


def rectangular_string(s: str) -> str:
    parts = s.split('.')
    out = [[]]
    for p in parts:
        if len('.'.join(out[-1])) > 15:
            out.append([])
        out[-1].append(p)
    return '\n'.join('.'.join(row) for row in out)

def rule_label(x: str):
    match = re.search(r"@rule\(([^()]+)\(.*\)\)", x)
    if not match:
        return None
    if match:
        extracted_string = match.group(1)
        qname = rectangular_string(extracted_string)
        return f'@rule\n{qname}'



# rule_label('@rule(pants.backend.python.util_rules.pex.create_pex(local_dists.pex))')


for node in graph.get_nodes():
    if node.get_name() == '51':
        print('found')
    current_label = node.get_label() if node.get_label() else node.get_name()
    current_label = current_label.strip('"')
    current_label = current_label.replace('\\"', '"')
    print(current_label)
    # new_label = current_label + "_modified"  # or any other label adjustment logic you want
    # node.set_label(new_label)
    parts = current_label.split(' == ')

    if len(parts) == 2:
        key, value = parts
        headline = rule_label(key) or key
        node.set_label(headline)
        tooltip = key + '\n\n' + value
        node.set('tooltip', tooltip)


with open('gsecrets/modified.003.dot', 'w') as f:
    f.write(graph.to_string())

# Then do:
# dot -Tpdf secrets/modified.003.dot > secrets/modified.003.pdf


# graph.write_dot('secrets/modified.003.dot')