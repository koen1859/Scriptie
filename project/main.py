from project.buildings import get_buildings
from project.db import get_addresses, get_road_data
from project.edges import get_edges
from project.find_beta import find_beta, scatterplot
from project.graph import make_graph
from project.map import create_map
from project.nodes import get_nodes
from project.read_tour import read_tours
from project.tsp import parrallel_solve_tsps

print("Importing the roads...")
roads = get_road_data()
print(f"{len(roads)} roads imported.")

print("Importing the buildings...")
building_data = get_addresses()
buildings = get_buildings(building_data)
print(f"{len(buildings)} buildings imported.")

print("Extracting all nodes...")
nodes = get_nodes(roads)
print(f"{len(nodes)} nodes extracted.")

print("Extracting all edges...")
edges, weights = get_edges(roads, nodes, buildings)
print(f"{len(edges)} edges extracted.")

print("Making the graph...")
graph = make_graph(nodes, buildings, edges, weights)
print(
    f"Graph has {len(graph.vs)} vertices and {len(graph.es)} edges. It contains {len(graph.components())} component(s)."
)

# print("Visualizing the road network on the map...")
# create_map(roads, "Groningen.html")

# print("Creating TSP instances...")
# create_tsps(graph, 10, range(10, 150, 2), 16)

print("Solving the TSPs...")
parrallel_solve_tsps(19)

print("Reading the output...")
tours, distances = read_tours()

# print("Visualizing some routes...")
# paths_subset(graph, nodes, buildings, tours, distances)

print("Finding beta and making scatter plot...")
x, y, b_hat, b = find_beta(distances)
scatterplot(distances, x, y, b_hat)
