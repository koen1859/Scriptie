from db import get_road_data, get_addresses
from nodes import get_nodes
from edges import get_edges
from graph import make_graph
from map import create_map
from create_tsp import create_parameter_file
from find_beta import find_beta
from run_simulation import run_simulation
from find_beta import find_beta, scatterplot
from pytictoc import TicToc

tic = TicToc()
tic.tic()

print("Importing the roads...")
roads = get_road_data()
print(f"{len(roads)} roads imported.")

print("Importing the buildings...")
buildings = get_addresses()
print(f"{len(buildings)} buildings imported.")

print("Extracting all nodes...")
nodes = get_nodes(roads)
print(f"{len(nodes)} nodes extracted.")

print("Extracting all edges...")
edges, weights = get_edges(roads, nodes)
print(f"{len(edges)} edges extracted.")

print("Making the graph...")
graph = make_graph(nodes, edges, weights)
print(f"Graph has {len(graph.vs)} vertices and {len(graph.es)} edges. It contains {len(graph.components())} component(s).")

tic.toc()

# print("Visualizing the road network on the map...")
# create_map(roads, "Groningen.html")

print("Making TSP parameter file...")
create_parameter_file()

print("Simulating TSPs...")
solutions, lengths = run_simulation(graph, nodes, 10, range(10, 100), False)

print("Finding beta and making scatter plot...")
x, y, b_hat = find_beta(lengths)
scatterplot(lengths, x, y, b_hat)

tic.toc()
