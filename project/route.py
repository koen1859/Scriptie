import folium
import math

def route(graph, start, end):
    path = [graph.vs[node]["name"] for node in graph.get_shortest_path(str(start), str(end), weights = "weight", output = "vpath")]
    return path

def plot_route(nodes, path, filename):
    m = folium.Map(location = nodes[int(path[math.ceil(len(path) / 2)])])
    path_coords = [nodes[int(index)] for index in path]
    folium.PolyLine(path_coords, color="red", weight=4.5).add_to(m)
    folium.Marker(nodes[int(path[0])], popup="House").add_to(m)
    folium.Marker(nodes[int(path[-1])], popup="Station").add_to(m)
    m.save(filename)
