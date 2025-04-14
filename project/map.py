import folium
import os


def create_map(
    roads: list[tuple[int, list[int], list[float], list[float], str]], filename: str
):
    os.makedirs("maps", exist_ok=True)
    m = folium.Map(location=[53.2194, 6.5665], zoom_start=12)

    for road in roads:
        trail_coordinates = list(zip(road[2], road[3]))
        folium.PolyLine(trail_coordinates, tooltip=str(road[0]), color="red").add_to(m)
    m.save(f"maps/{filename}")
