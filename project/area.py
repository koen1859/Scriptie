from shapely import union_all
from shapely.geometry import Point, MultiPoint
import geopandas as gpd


def get_area(buildings):
    points = [tuple(map(float, coord)) for coord in buildings.values()]
    gdf = gpd.GeoDataFrame(
        geometry=[Point(lon, lat) for lat, lon in points], crs="EPSG:4326"
    ).to_crs("EPSG:28992")
    hull = union_all(gdf).convex_hull
    return hull.area / 1000000
