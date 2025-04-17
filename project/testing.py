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
from find_beta import find_beta, scatterplot, errorsplot
from map import create_map

roads = get_road_data("groningen", "Binnenstad")
print(f"{len(roads)} roads imported.")
building_data = get_addresses("groningen", "Binnenstad")
buildings, building_DB = get_buildings(building_data)
print(f"{len(buildings)} buildings imported.")
create_map(roads, f"{"groningen"}_{"Binnenstad"}.html", buildings)
nodes = get_nodes(roads)
print(f"{len(nodes)} nodes extracted.")
edges, weights = get_edges(roads, nodes, buildings)
print(f"{len(edges)} edges extracted.")
graph = make_graph(nodes, buildings, building_DB, edges, weights)
area = get_area(buildings)
print(area)
