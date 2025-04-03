from graph import distance
from shapely.geometry import Point
from shapely.strtree import STRtree


def get_edges(
    roads: list[tuple[int, list[int], list[float], list[float], str]],
    nodes: dict[str, tuple[float, float]],
    buildings: dict[str, tuple[float, float]],
) -> tuple[list[tuple[str, str]], list[float]]:
    edges: list[tuple[str, str]] = []
    weights: list[float] = []
    for road in roads:
        road_nodes = [str(id) for id in road[1]]
        oneway = road[4]

        for i in range(1, len(road_nodes)):
            edges.append((road_nodes[i - 1], road_nodes[i]))
            weights.append(distance(nodes[road_nodes[i - 1]], nodes[road_nodes[i]]))
            if oneway != "yes":
                edges.append((road_nodes[i], road_nodes[i - 1]))
                weights.append(distance(nodes[road_nodes[i]], nodes[road_nodes[i - 1]]))

    node_points = [Point(coords) for coords in nodes.values()]
    point_to_node_id = {i: node_id for i, node_id in enumerate(list(nodes.keys()))}

    tree = STRtree(node_points)
    for building_id, building_coords in buildings.items():
        building_point = Point(building_coords)
        nearest_node_point = tree.nearest(building_point)
        nearest_node_id = point_to_node_id[nearest_node_point]

        edges.append((str(building_id), str(nearest_node_id)))
        weights.append(distance(building_coords, nodes[nearest_node_id]))
        edges.append((str(nearest_node_id), str(building_id)))
        weights.append(distance(nodes[nearest_node_id], building_coords))

    return edges, weights
