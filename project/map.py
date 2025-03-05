import folium

def create_map(roads, filename):
    m = folium.Map(location=[53.2194, 6.5665], zoom_start=12)

    for road in roads:
        trail_coordinates = list(zip(road[2], road[3]))
        folium.PolyLine(trail_coordinates, tooltip = str(road[0])).add_to(m)
    m.save(filename)
