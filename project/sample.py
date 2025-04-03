import random
import igraph as ig
from typing import Union, List


def sample(graph: ig.Graph, size: int, cities: Union[str, List[str]]) -> List[str]:
    if cities == "Any":
        building_names = [v["name"] for v in graph.vs if v["is_building"] == 1]
    else:
        if isinstance(cities, str):
            cities = [cities]
        building_names = [
            v["name"] for v in graph.vs if v["is_building"] == 1 and v["city"] in cities
        ]
    return random.sample(building_names, size)
