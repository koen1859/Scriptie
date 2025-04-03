import json
import multiprocessing
import os
import subprocess

from distance_dict import distance_dict
from sample import sample


def generate_tsp(graph, i, run, city, dirname):
    locations = sample(graph, i, city)
    distances = distance_dict(graph, locations)
    index_to_location = {idx + 1: loc for idx, loc in enumerate(locations)}

    os.makedirs(dirname, exist_ok=True)

    with open(f"{dirname}/problem_{i}_{run}.tsp", "w") as f:
        f.write("NAME : tsp_problem\n")
        f.write("TYPE : TSP\n")
        f.write(f"DIMENSION : {len(locations)}\n")
        f.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
        f.write("EDGE_WEIGHT_FORMAT : FULL_MATRIX\n")
        f.write("EDGE_WEIGHT_SECTION\n")

        for loc1 in locations:
            row = [str(int(distances[(loc1, loc2)])) for loc2 in locations]
            f.write(" ".join(row) + "\n")
        f.write("EOF\n")

    with open(f"{dirname}/index_to_location_{i}_{run}.json", "w") as f:
        json.dump(index_to_location, f)

    with open(f"{dirname}/problem_{i}_{run}.par", "w") as f:
        f.write(f"PROBLEM_FILE = {dirname}/problem_{i}_{run}.tsp\n")
        f.write(f"OUTPUT_TOUR_FILE = {dirname}/tour_{i}_{run}.txt\n")


def create_tsps(graph, num_runs, num_locations, num_threads, city, dirname):
    tasks = [
        (graph, i, run, city, dirname) for i in num_locations for run in range(num_runs)
    ]

    with multiprocessing.Pool(num_threads) as pool:
        pool.starmap(generate_tsp, tasks)


def solve_tsp(parameter_file, dirname):
    subprocess.run(["LKH", f"{dirname}/{parameter_file}"], check=True)


def parrallel_solve_tsps(num_threads, dirname):
    tasks = [(f, dirname) for f in os.listdir(dirname) if f.endswith(".par")]

    with multiprocessing.Pool(num_threads) as pool:
        pool.starmap(solve_tsp, tasks)
