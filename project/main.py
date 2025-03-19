from buildings import get_buildings
from db import get_addresses, get_road_data
from edges import get_edges
from find_beta import find_beta, scatterplot
from graph import make_graph
from nodes import get_nodes
from pytictoc import TicToc
from read_tour import read_tours
from tsp import parrallel_solve_tsps

tic = TicToc()
tic.tic()

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

tic.toc()
tic.tic()

# print("Visualizing the road network on the map...")
# create_map(roads, "Groningen.html")

# print("Creating TSP instances...")
# create_tsps(graph, 100, range(10, 90, 2))
# tic.toc()
# tic.tic()

print("Solving the TSPs...")
parrallel_solve_tsps(19)
tic.toc()
tic.tic()

print("Reading the output...")
tours, distances = read_tours()

# print("Visualizing some routes...")
# paths_subset(graph, nodes, buildings, tours, distances)

print("Finding beta and making scatter plot...")
x, y, b_hat, b = find_beta(distances)
tic.toc()
scatterplot(distances, x, y, b_hat)
