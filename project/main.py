from db import get_road_data
from nodes import get_nodes
from graph import make_graph
from map import create_map
from create_tsp import create_parameter_file, create_tsp
from project.route import plot_route, route
from solve_tsp import solve_tsp
from read_tour import read_tour

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
create_map(roads, "Groningen.html")

print("Making TSP parameter file...")
create_parameter_file()

print("Making a TSP...")
distances = create_tsp(graph, 100)

print("Solving the TSP...")
solve_tsp()

print("Reading the output...")
locations, distance = read_tour()

print("Visualizing the TSP Path...")
path = route(graph, locations)
plot_route(nodes, locations, path, distance, "TSP.html")
