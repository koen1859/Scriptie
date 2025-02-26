from db import get_road_data
from nodes import get_nodes
from graph import make_graph
from map import create_map
from route import route, plot_route

print("Importing the roads...")
roads = get_road_data()
print(f"{len(roads)} roads imported.")

print("Extracting all nodes...")
nodes = get_nodes(roads)
print(f"{len(nodes)} nodes extracted.")

print("Making the graph...")
graph = make_graph(roads, nodes)
print(f"Graph has {len(graph.vs)} vertices and {len(graph.es)} edges. It contains {len(graph.components())} component(s).")

print("Visualizing the road network on the map...")
create_map(graph, nodes, "Groningen.html")

house_station = route(graph, 10606779735, 2303887045)
house_zernike = route(graph, 10606779735, 1201758528)
plot_route(nodes, house_station, "house_station.html")
plot_route(nodes, house_zernike, "house_zernike.html")
