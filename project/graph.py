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

def make_graph(roads, nodes):
    graph = ig.Graph(directed = False)
    used_ids = set()

    for _, node_ids, _, _ in roads:
        for node_id in node_ids:
            if node_id not in used_ids:
                graph.add_vertex(name=str(node_id), coords=nodes[node_id])
                used_ids.add(node_id)

        for i in range(1, len(node_ids)):
            graph.add_edge(str(node_ids[i - 1]), str(node_ids[i]), weight = distance(nodes[node_ids[i - 1]], nodes[node_ids[i]]))

    return graph.subgraph(max(graph.components(), key = len))
