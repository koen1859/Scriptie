from db import get_addresses, get_road_data
from area import get_area
from map import create_map
from buildings import get_buildings
from nodes import get_nodes
from edges import get_edges
from graph import make_graph
from tsp import create_tsps, parrallel_solve_tsps
from read_tour import read_tours
from route import paths_subset
from find_beta import find_beta, results, scatterplot, errorsplot
from map import create_map

# This is just a file i made to test some things before but it will probably return error now
roads = get_road_data("groningen", "Rivierenbuurt")
print(f"{len(roads)} roads imported.")
building_data = get_addresses("groningen", "Rivierenbuurt")
buildings, building_DB = get_buildings(building_data)
print(f"{len(buildings)} buildings imported.")
create_map(roads, f"{"groningen"}_{"Rivierenbuurt"}.html", buildings)
nodes = get_nodes(roads)
print(f"{len(nodes)} nodes extracted.")
edges, weights = get_edges(roads, nodes, buildings)
print(f"{len(edges)} edges extracted.")
graph = make_graph(nodes, buildings, building_DB, edges, weights)
area = get_area(buildings)
tours, lengths = read_tours("tsps_groningen_Rivierenbuurt")
x, y, b_hat, b_hat_n = find_beta(lengths, area)
line, errors, MAE = results(lengths, x, y, b_hat, area)
scatterplot(lengths, x, y, b_hat, area, "scatter_groningen_Rivierenbuurt")
errorsplot(lengths, x, y, b_hat, area, "errors_groningen_Rivierenbuurt")
print(MAE)
