def get_nodes(roads):
    nodes = {}
    for _, node_ids, node_lats, node_lons, _ in roads:
        for i in range(len(node_ids)):
            nodes[str(node_ids[i])] = (node_lats[i], node_lons[i])
    return nodes
