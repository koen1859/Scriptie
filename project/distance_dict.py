def distance_dict(graph, locations):
    distances = {}
    all_shortest_paths = graph.shortest_paths_dijkstra(
        source=locations, target=locations, weights="weight"
    )
    for i, source in enumerate(locations):
        for j, target in enumerate(locations):
            distances[(source, target)] = all_shortest_paths[i][j]
    return distances
