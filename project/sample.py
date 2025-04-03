import random
import igraph as ig


def sample(graph: ig.Graph, size: int, city: str) -> list[str]:
    building_names: list[str] = [
        v["name"] for v in graph.vs if v["is_building"] == 1 and v["city"] == city
    ]
    return random.sample(building_names, size)
