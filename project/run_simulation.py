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


def run_simulation(DB, neighborhood):
    roads = get_road_data(DB, neighborhood)
    print(f"{len(roads)} roads imported.")
    building_data = get_addresses(DB, neighborhood)
    buildings, building_DB = get_buildings(building_data)
    print(f"{len(buildings)} buildings imported.")
    # create_map(roads, f"{DB}_{neighborhood}.html", buildings)
    nodes = get_nodes(roads)
    print(f"{len(nodes)} nodes extracted.")
    edges, weights = get_edges(roads, nodes, buildings)
    print(f"{len(edges)} edges extracted.")
    graph = make_graph(nodes, buildings, building_DB, edges, weights)
    print(
        f"Graph has {len(graph.vs)} vertices and {len(graph.es)} edges. It contains {len(graph.components())} component(s)."
    )
    create_tsps(graph, 10, range(10, 90, 1), 100, "Any", f"tsps_{DB}_{neighborhood}")
    parrallel_solve_tsps(19, f"tsps_{DB}_{neighborhood}")
    tours, distances = read_tours(f"tsps_{DB}_{neighborhood}")
    area = get_area(buildings)
    # paths_subset(graph, nodes, buildings, tours, distances, DB)
    x, y, b_hat, b = find_beta(distances, area)
    scatterplot(distances, x, y, b_hat, area, f"scatter_{DB}_{neighborhood}")
    errorsplot(distances, x, y, b_hat, area, f"errors_{DB}_{neighborhood}")
    return b_hat
