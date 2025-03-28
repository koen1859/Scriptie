import json

from project.distance_dict import distance_dict
from project.sample import sample


def create_parameter_file():
    with open("tsps/problem.par", "w") as f:
        f.write("PROBLEM_FILE = tsps/problem.tsp\n")
        f.write("OUTPUT_TOUR_FILE = tsps/tour.txt\n")


def create_tsp(graph, size):
    locations = sample(graph, size)
    distances = distance_dict(graph, locations)
    index_to_location = {i + 1: loc for i, loc in enumerate(locations)}

    with open("tsps/problem.tsp", "w") as f:
        f.write("NAME : tsp_problem\n")
        f.write("TYPE : TSP\n")
        f.write(f"DIMENSION : {len(locations)}\n")
        f.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT : FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")

        for loc1 in locations:
            row = []
            for loc2 in locations:
                row.append(str(int(distances[(loc1, loc2)])))
            f.write(" ".join(row) + "\n")
        f.write("EOF\n")

    with open("tsps/index_to_location.json", "w") as f:
        json.dump(index_to_location, f)
    return distances
