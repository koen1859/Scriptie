from graph import distance
def get_edges(roads, nodes):
    edges = []
    weights = []
    for road in roads:
        road_nodes = [str(id) for id in road[1]]
        oneway = road[4]

        for i in range(1, len(road_nodes)):
            edges.append((road_nodes[i - 1], road_nodes[i]))
            weights.append(distance(nodes[road_nodes[i - 1]], nodes[road_nodes[i]]))
            if oneway != "yes":
                edges.append((road_nodes[i], road_nodes[i - 1]))
                weights.append(distance(nodes[road_nodes[i]], nodes[road_nodes[i - 1]]))
    return edges, weights
