import ujson
import multiprocessing
import os
import subprocess

from distance_dict import distance_dict
from sample import sample


# This function generates a .tsp, .par and .json file to write to the disk, so LKH can solve
# the TSP later. First we take a random sample of the buildings, then create distance dictionary
# between these buildings. Also, a mapping is made to map 1,2,3,... back to the correct building
# indices since LKH can only use indices starting from 1 but we already have building indices
# from openstreetmap.
def generate_tsp(graph, i, run, city, dirname):
    locations = sample(graph, i, city)
    distances = distance_dict(graph, locations)
    index_to_location = {idx + 1: loc for idx, loc in enumerate(locations)}

    header = [
        "NAME : tsp_problem",
        "TYPE : TSP",
        f"DIMENSION : {len(locations)}",
        "EDGE_WEIGHT_TYPE : EXPLICIT",
        "EDGE_WEIGHT_FORMAT : FULL_MATRIX",
        "EDGE_WEIGHT_SECTION",
    ]
    rows = []

    for loc1 in locations:
        row = [str(int(distances[(loc1, loc2)])) for loc2 in locations]
        rows.append(" ".join(row))

    body = "\n".join(header + rows + ["EOF"])

    with open(f"{dirname}/problem_{i}_{run}.tsp", "w") as f:
        f.write(body)

    with open(f"{dirname}/index_to_location_{i}_{run}.json", "w") as f:
        ujson.dump(index_to_location, f)

    with open(f"{dirname}/problem_{i}_{run}.par", "w") as f:
        f.write(f"PROBLEM_FILE = {dirname}/problem_{i}_{run}.tsp\n")
        f.write(f"OUTPUT_TOUR_FILE = {dirname}/tour_{i}_{run}.txt\n")


# if we would write all tsps sequentially, it would take ages upon ages. We use multiprocessing
# to speed it up.
def create_tsps(graph, num_runs, num_locations, num_threads, city, dirname):
    os.makedirs(dirname, exist_ok=True)
    tasks = [
        (graph, i, run, city, dirname) for i in num_locations for run in range(num_runs)
    ]

    with multiprocessing.Pool(num_threads) as pool:
        pool.starmap(generate_tsp, tasks)


# This function runs the Lin-Kernighan heuristic to solve the tsps. We do not want the output
# to display since it gives a lot of output that is not so useful to us, and in the simulation
# some information is printed, this would not be easy to read when there is a lot of stuff
# below and under it we do not need.
def solve_tsp(parameter_file, dirname):
    subprocess.run(
        ["LKH", f"{dirname}/{parameter_file}"], stdout=subprocess.DEVNULL, check=True
    )


# We make sure that each core on the system solves 1 at the time TSP to speed up the process.
def parrallel_solve_tsps(dirname):
    num_threads = multiprocessing.cpu_count()
    par_files = [f for f in os.listdir(dirname) if f.endswith(".par")]
    tasks = [(f, dirname) for f in par_files]
    chunksize = max(1, len(tasks) // (num_threads * 4))

    with multiprocessing.Pool(num_threads) as pool:
        pool.starmap(solve_tsp, tasks, chunksize=chunksize)
