def get_buildings(
    building_data: list[tuple[int, float, float]],
) -> dict[str, tuple[float, float]]:
    buildings: dict[str, tuple[float, float]] = {}
    for id, lat, lon in building_data:
        buildings[str(id)] = (lat, lon)
    return buildings
