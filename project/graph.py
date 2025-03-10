import igraph as ig
from math import radians, cos, sqrt

def distance(node1, node2):
    # Earth’s radius in meters
    R = 6371000
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [node1[0], node1[1], node2[0], node2[1]])
    # Approximation of small distance on a sphere
    x = (lon2 - lon1) * cos((lat1 + lat2) / 2)
    y = lat2 - lat1
    return R * sqrt(x**2 + y**2)

def make_graph(nodes, edges, weights):
    graph = ig.Graph(directed = True)

    node_names = list(nodes.keys())
    coords = list(nodes.values())
    graph.add_vertices(node_names)
    graph.vs["coords"] = coords

    name_to_index = {name: idx for idx, name in enumerate(node_names)}
    edge_indices = [(name_to_index[u], name_to_index[v]) for u, v in edges]

    graph.add_edges(edge_indices)
    graph.es["weight"] = weights

    return graph.subgraph(max(graph.components(), key = len))
