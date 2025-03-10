import random

# def sample(graph, size):
#     return random.sample(list(graph.vs["name"]), size)

def sample(graph, size):
    building_names = [v["name"] for v in graph.vs if v["is_building"] == 1]
    return random.sample(building_names, size)
