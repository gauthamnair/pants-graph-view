import itertools
import json
import re

import pydot
import networkx as nx

infile = 'gsecrets/graph.003.dot'

graphs = pydot.graph_from_dot_file(infile)

graph = graphs[0]

nodes = graph.get_nodes()

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

roots = [x for x in nxg.nodes() if nxg.in_degree(x) == 0]

print(len(nodes))
print(len(nxg))

depth_limit = 2

succ = dict(nx.bfs_successors(nxg, source='14', depth_limit=5))
# succ = {}
# for s in nx.bfs_successors(nxg, source='14', depth_limit=2):
#     succ[s] = nxg.nodes[s]

nodes_to_include = set(itertools.chain(*succ.values()))
nodes_to_include.add('14')

subg = nxg.subgraph(nodes_to_include)


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


def node_json(node_id, g):
    node = g.nodes[node_id]
    value = node['value']
    out = {
        '_node_id': node_id,
        'key': node['key'],
        'value': value,
    }
    out.update(rule_label(node['key']))

    neighbors = list(g.successors(node_id))
    if neighbors:
        out['neighbors'] = [node_json(v, g) for v in neighbors]

    return out

j = node_json('14', subg)


with open('gsecrets/jout.json', 'w') as f:
    json.dump(j, f, indent=2)


def graph_json(g: nx.DiGraph):
    roots = [x for x in g.nodes() if g.in_degree(x) == 0]

    nodes = []
    for node_id, ndata in g.nodes.data():
        jnode = {
            '_node_id': node_id,
            'key': ndata['key'],
            'value': ndata['value']
        }
        if 'RunId' in ndata['key']:
            print(jnode)
        jnode.update(rule_label(ndata['key']))
        jnode.update(parse_value_type(ndata['value']))
        jnode['neighbors'] = list(g.successors(node_id))
        nodes.append(jnode)

    return {
        'roots': roots,
        'nodes': nodes
    }

jgraph = graph_json(nxg)

with open('gsecrets/graph.json', 'w') as f:
    json.dump(jgraph, f)

print('')
