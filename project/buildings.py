def get_buildings(building_data):
    buildings = {}
    for id, lat, lon in building_data:
        buildings[str(id)] = (lat, lon)
    return buildings
