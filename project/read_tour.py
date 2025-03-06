import json

def read_tour():
    with open("tsps/index_to_location.json", "r") as f:
        index_to_location = json.load(f)

    with open("tsps/tour.txt", "r") as f:
        lines = f.readlines()

    start = lines.index("TOUR_SECTION\n") + 1
    end = lines.index("-1\n")

    tour_indices = [str(int(node)) for node in lines[start:end]]
    tour_locations = [index_to_location[node] for node in tour_indices]

    length_line = next(line for line in lines if line.startswith("COMMENT : Length"))
    distance = int(length_line.split('=')[1].strip())

    return tour_locations, distance
