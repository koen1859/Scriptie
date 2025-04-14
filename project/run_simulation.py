from db import get_addresses, get_road_data
from buildings import get_buildings
from nodes import get_nodes
from edges import get_edges
from graph import make_graph
from tsp import create_tsps, parrallel_solve_tsps
from read_tour import read_tours
from route import paths_subset
from find_beta import find_beta, scatterplot, errorsplot


def run_simulation(DB_NAME, city):
    roads = get_road_data()
    building_data = get_addresses()
    buildings, building_city = get_buildings(building_data)
    nodes = get_nodes(roads)
    edges, weights = get_edges(roads, nodes, buildings)
    graph = make_graph(nodes, buildings, building_city, edges, weights)
    create_tsps(graph, 50, range(10, 70, 1), 100, "Any", "tsps_all")
    parrallel_solve_tsps(19, "tsps_all")
    tours, distances = read_tours("tsps_all")
    paths_subset(graph, nodes, buildings, tours, distances, "all")
    x, y, b_hat, b = find_beta(distances, 2316)
    scatterplot(distances, x, y, b_hat, 2316, "scatter_all")
    errorsplot(distances, x, y, b_hat, 2316, "errors_all")
