import folium
import math

def route(graph, locations):
    path = []
    for i in range(len(locations)):
        path_vertices = graph.get_shortest_path(locations[i - 1], locations[i], weights="weight", output="vpath")
        path.extend([graph.vs[node]["name"] for node in path_vertices])
    return path

def plot_route(nodes, locations, path, distance, filename):
    m = folium.Map(location = nodes[path[math.ceil(len(path) / 2)]])
    path_coords = [nodes[index] for index in path]
    folium.PolyLine(path_coords, color="red", weight=4.5).add_to(m)
    for i in range(len(locations)):
        folium.Marker(nodes[locations[i]], popup=f"The total route distance is {round(distance / 1000, 3)}km.").add_to(m)
    m.save(f"maps/{filename}")
