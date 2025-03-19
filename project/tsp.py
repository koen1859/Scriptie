import json
import multiprocessing
import os
import subprocess

from distance_dict import distance_dict
from sample import sample


def create_tsps(graph, num_runs, num_locations):
    for i in num_locations:
        for run in range(num_runs):
            locations = sample(graph, i)
            distances = distance_dict(graph, locations)
            index_to_location = {i + 1: loc for i, loc in enumerate(locations)}

            with open(f"tsps/problem_{i}_{run}.tsp", "w") as f:
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

            with open(f"tsps/index_to_location_{i}_{run}.json", "w") as f:
                json.dump(index_to_location, f)

            with open(f"tsps/problem_{i}_{run}.par", "w") as f:
                f.write(f"PROBLEM_FILE = tsps/problem_{i}_{run}.tsp\n")
                f.write(f"OUTPUT_TOUR_FILE = tsps/tour_{i}_{run}.txt\n")


def solve_tsp(parameter_file):
    subprocess.run(["LKH", f"tsps/{parameter_file}"], check=True)


def parrallel_solve_tsps(num_threads):
    par_files = [f for f in os.listdir("tsps/") if f.endswith(".par")]

    with multiprocessing.Pool(num_threads) as pool:
        pool.map(solve_tsp, par_files)
