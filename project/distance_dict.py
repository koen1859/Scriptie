# import itertools as iter

# def distance_dict(graph, locations):
#     combs = list(iter.permutations(locations, 2))
#     distances = {}
#     for comb in combs:
#         distances[comb] = sum(graph.es[edge]["weight"] for edge in graph.get_shortest_path(str(comb[0]), str(comb[1]), weights="weight", output="epath"))
#     for location in locations:
#         distances[(location, location)] = 0
#     return distances

def distance_dict(graph, locations):
    distances = {}
    all_shortest_paths = graph.shortest_paths_dijkstra(source=locations, target=locations, weights="weight")
    for i, source in enumerate(locations):
        for j, target in enumerate(locations):
            distances[(source, target)] = all_shortest_paths[i][j]
    return distances
