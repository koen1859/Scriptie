def get_buildings(
    building_data: list[tuple[int, float, float, str]],
) -> tuple[dict[str, tuple[float, float]], dict[str, str]]:
    buildings: dict[str, tuple[float, float]] = {}
    building_city: dict[str, str] = {}
    for id, lat, lon, city in building_data:
        buildings[str(id)] = (lat, lon)
        building_city[str(id)] = city
    return buildings, building_city
