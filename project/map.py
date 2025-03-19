import folium
import numpy as np


def create_folium_map(nodes, edges, buildings, map_path="graph_map.html"):
    # Extract node coordinates for centering the map
    all_nodes = {**nodes, **buildings}
    node_coords = np.array(list(all_nodes.values()))
    center_lat = np.mean(node_coords[:, 0])
    center_lon = np.mean(node_coords[:, 1])

    # Initialize a folium map centered around the average coordinates of nodes
    folium_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)

    # Add edges to the map
    for start, end in edges:
        start_coords = all_nodes[start]
        end_coords = all_nodes[end]
        points = [start_coords, end_coords]
        folium.PolyLine(points, color="blue", weight=1).add_to(folium_map)

    # Save the map to an HTML file
    folium_map.save(map_path)
    print(f"Map saved to {map_path}")


def create_map(roads, filename):
    m = folium.Map(location=[53.2194, 6.5665], zoom_start=12)

    for road in roads:
        trail_coordinates = list(zip(road[2], road[3]))
        folium.PolyLine(trail_coordinates, tooltip=str(road[0]), color="red").add_to(m)
    m.save(f"maps/{filename}")
