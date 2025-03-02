import folium

def create_map(graph, nodes, filename):
    m = folium.Map(location=[53.2194, 6.5665], zoom_start=12)

    for edge in graph.es:
        start_node = graph.vs[edge.source]["name"]
        end_node = graph.vs[edge.target]["name"]

        start_coords = nodes[int(start_node)]
        end_coords = nodes[int(end_node)]

        folium.PolyLine(
            locations = [start_coords, end_coords],
            color = "red",
            weight = 2.5,
            opacity = 1
        ).add_to(m)
    m.save(filename)
