import random

def sample(graph, size):
    return random.sample(list(graph.vs["name"]), size)
