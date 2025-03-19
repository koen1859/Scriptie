import folium


def route(graph, locations):
    path = []
    for i in range(len(locations)):
        path_vertices = graph.get_shortest_path(
            locations[i - 1], locations[i], weights="weight", output="vpath"
        )
        path.extend([graph.vs[node]["name"] for node in path_vertices])
    return path


def plot_route(nodes, buildings, locations, path, distance, filename):
    m = folium.Map(location=[53.2194, 6.5665], zoom_start=12)
    all_nodes = {**nodes, **buildings}
    path_coords = [all_nodes[index] for index in path]
    folium.PolyLine(path_coords, color="red", weight=4.5).add_to(m)
    for i in range(len(locations)):
        folium.Marker(
            all_nodes[locations[i]],
            popup=f"The total route distance is {round(distance / 1000, 3)}km.",
        ).add_to(m)
    m.save(f"maps/{filename}")


def paths_subset(graph, nodes, buildings, tours, distances):
    for i in tours.keys():
        locations = tours[i][0]
        distance = distances[i][0]
        path = route(graph, locations)
        plot_route(nodes, buildings, locations, path, distance, f"TSP_{i}.html")
