import json
import re
import pydot
import networkx as nx
from importlib import resources


def read_dot_file_to_nx_graph(file_name: str) -> nx.DiGraph:
    graph = pydot.graph_from_dot_file(file_name)[0]
    nxg = nx.DiGraph()

    for n in graph.get_nodes():
        label = n.get_label() or n.get_name()
        label = label.strip('"')
        parts = label.split(' == ', 1)
        if len(parts) >= 2:
            key, value = parts
        else:
            key, value = label, None
        nxg.add_node(n.get_name(), key=key, value=value)

    for e in graph.get_edges():
        nxg.add_edge(e.get_source(), e.get_destination())

    return nxg


def rule_label(x: str):
    match = re.search(r"@rule\(([^()]+)\((.*)\)\)", x)
    if not match:
        return {
            'rule_func': None,
            'rule_args': None,
            'rule_short_name': None,
        }
    if match:
        return {
            'rule_func': match.group(1),
            'rule_args': match.group(2),
            'rule_short_name': match.group(1).split('.')[-1],
        }


def parse_value_type(x):
    # repr match like 'Value(<pants.core.goals.test.TestSubsystem object at 0x1057c7f40>)'
    # to return TestSubsystem
    m = re.search(r"^Value\(<([^>\s]*)", x)
    if m:
        return {'output_type': m.group(1).split('.')[-1]}

    # match to a dataclass value
    # like Value(Test(exit_code=0))
    m = re.search(r"^Value\(([^(]*)\(", x)
    if m:
        return {'output_type': m.group(1)}

    m = re.search(r"^([^(\s<]+)\(", x)
    if m:
        return {'output_type': m.group(1)}

    return {'output_type': None}


def nx_graph_to_jsonable_data(g: nx.DiGraph) -> dict:
    roots = [x for x in g.nodes() if g.in_degree(x) == 0]

    nodes = {}
    for node_id, ndata in g.nodes.data():
        jnode = {
            '_node_id': node_id,
            'key': ndata['key'],
            'value': ndata['value']
        }
        jnode.update(rule_label(ndata['key']))
        jnode.update(parse_value_type(ndata['value']))
        jnode['neighbors'] = list(g.successors(node_id))
        nodes[node_id] = jnode

    return {
        'roots': roots,
        'nodes': nodes
    }


def main(input_file_name: str, output_file_name: str):
    g = read_dot_file_to_nx_graph(input_file_name)
    j = nx_graph_to_jsonable_data(g)

    h_template = resources.read_text(__package__, 'viewer_template.html')
    h = h_template.replace('INSERT_DATA_HERE', json.dumps(j))

    with open(output_file_name, 'w') as fout:
        print(f'Writing to {output_file_name}')
        fout.write(h)
