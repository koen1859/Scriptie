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


# This function writes all .par, .tsp, .json files to be able to solve and analyze the
# TSPs with LKH. This is put in a separate function since I wanted to be able to only make
# the problems first, and solve them afterwards, separately.
def write_tsps(DB, neighborhood):
    roads = get_road_data(DB, neighborhood)
    print(f"{len(roads)} roads imported.")
    building_data = get_addresses(DB, neighborhood)
    buildings, building_DB = get_buildings(building_data)
    print(f"{len(buildings)} buildings imported.")
    create_map(roads, f"{DB}_{neighborhood}.html", buildings)
    nodes = get_nodes(roads)
    print(f"{len(nodes)} nodes extracted.")
    edges, weights = get_edges(roads, nodes, buildings)
    print(f"{len(edges)} edges extracted.")
    graph = make_graph(nodes, buildings, edges, weights)
    print(
        f"""Graph has {len(graph.vs)} vertices and {len(graph.es)} edges.\n
        It contains {len(graph.components())} component(s)."""
    )
    # We set num_cores to 28 here since the creation of tsps doesnt use that much CPU, but a
    # lot of disk I/O so it is a lot faster to have a lot more processes than threads
    # each thread can easily do a lot more than 1 at the time.
    create_tsps(graph, 100, range(20, 90, 2), 28, "Any", f"tsps_{DB}_{neighborhood}")


# This function runs LKH to solve the tsps we made before, and it analyzes the results
def run_simulation(DB, neighborhood):
    building_data = get_addresses(DB, neighborhood)
    buildings, building_DB = get_buildings(building_data)
    parrallel_solve_tsps(f"tsps_{DB}_{neighborhood}")
    tours, distances = read_tours(f"tsps_{DB}_{neighborhood}")
    area = get_area(buildings)
    # paths_subset(graph, nodes, buildings, tours, distances, DB)
    x, y, b_hat, b = find_beta(distances, area)
    line, errors, MAE = results(distances, x, y, b, area)
    scatterplot(distances, x, y, b_hat, line, f"scatter_{DB}_{neighborhood}")
    errorsplot(errors, f"errors_{DB}_{neighborhood}")
    return b_hat, MAE
