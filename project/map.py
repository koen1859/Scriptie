import folium
import os

# This function creates a map of the roads that were imported from the postgres database.
# def create_map(roads, filename, buildings):
#     os.makedirs("maps", exist_ok=True)
#     m = folium.Map(location=[53.2194, 6.5665], zoom_start=12)
#
#     for road in roads:
#         trail_coordinates = list(zip(road[2], road[3]))
#         folium.PolyLine(trail_coordinates, tooltip=str(road[0]), color="red").add_to(m)
#     for building in buildings.values():
#         folium.Marker(building).add_to(m)
#     m.save(f"maps/{filename}")


def create_map(nodes, buildings, graph, filename):
    os.makedirs("maps", exist_ok=True)
    all_nodes = {**nodes, **buildings}
    edges = [
        (graph.vs[edge.source]["name"], graph.vs[edge.target]["name"])
        for edge in graph.es
    ]
    m = folium.Map(location=list(nodes[edges[0][0]]))
    for edge in edges:
        coords = list((all_nodes[edge[0]], all_nodes[edge[1]]))
        folium.PolyLine(coords, color="red").add_to(m)
    m.save(f"maps/{filename}")
