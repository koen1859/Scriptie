from db import get_addresses, get_road_data
from buildings import get_buildings
from nodes import get_nodes
from edges import get_edges
from graph import make_graph
from map import create_map
from tsp import create_tsps, parrallel_solve_tsps, parroosterpoortel_solve_tsps
from read_tour import read_tours
from route import paths_subset
from find_beta import find_beta, scatterplot, errorsplot

print("Importing the roads...")
roads = get_road_data()
print(f"{len(roads)} roads imported.")

print("Importing the buildings...")
building_data = get_addresses()
buildings, building_city = get_buildings(building_data)
print(f"{len(buildings)} buildings imported.")

print("Extracting oosterpoort nodes...")
nodes = get_nodes(roads)
print(f"{len(nodes)} nodes extracted.")

print("Extracting oosterpoort edges...")
edges, weights = get_edges(roads, nodes, buildings)
print(f"{len(edges)} edges extracted.")

print("Making the graph...")
graph = make_graph(nodes, buildings, building_city, edges, weights)
print(
    f"Graph has {len(graph.vs)} vertices and {len(graph.es)} edges. It contains {len(graph.components())} component(s)."
)

print("Visualizing the road network on the map...")
create_map(roads, "Oosterpoort.html")

print("Creating TSP instances...")
create_tsps(graph, 10, range(10, 70, 1), 100, "Any", "tsps_oosterpoort")

print("Solving the TSPs...")
parrallel_solve_tsps(19, "tsps_all")

print("Reading the output...")
tours, distances = read_tours("tsps_oosterpoort")

print("Visualizing some routes...")
paths_subset(graph, nodes, buildings, tours, distances, "oosterpoort")

print("Finding beta and making scatter plot...")
x, y, b_hat, b = find_beta(distances, 2316)
scatterplot(distances, x, y, b_hat, 2316, "scatter_oosterpoort")
errorsplot(distances, x, y, b_hat, 2316, "errors_oosterpoort")
