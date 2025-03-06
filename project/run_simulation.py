from create_tsp import create_tsp
from solve_tsp import solve_tsp
from read_tour import read_tour
from route import route, plot_route

def run_simulation(graph, nodes, num_runs, num_locations, plot):
    solutions, lengths = {}, {}
    for i in num_locations:
        solutions[i], lengths[i] = [], []
        for j in range(num_runs):
            create_tsp(graph, i)
            solve_tsp()
            solution, length = read_tour()
            solutions[i].append(solution)
            lengths[i].append(length)

            if plot == True:
                path = route(graph, solution)
                plot_route(nodes, solution, path, length, f"TSP_{i}_{j}.html")

    return solutions, lengths
