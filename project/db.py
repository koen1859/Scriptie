import psycopg2
from config import DB_HOST, DB_PORT, DB_USER


# This function imports the roads from the database. It works as follows:
# we fetch a quarter from the polygon table, fetch all roads that satisfy a set of types
# and that are either: fully contained in the polygon, or partly in and partly outside of
# the polygon (i.e.  intersects the boundary). In this case we still fetch that entire road,
# also the parts that are not in the neighborhood. This is done because otherwise there are
# some edge cases where connections are missed that should have been there.
def get_road_data(DB, neighborhood):
    connection = psycopg2.connect(dbname=DB, user=DB_USER, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        WITH neighborhood AS (
            SELECT ST_Transform(way, 4326) AS geom
            FROM planet_osm_polygon
            WHERE place = 'quarter'
            AND name = '{neighborhood}'
        ),
        road_geometries AS (
            SELECT
                w.id AS road_id,
                w.nodes AS node_ids,
                w.tags->>'oneway' AS oneway
            FROM planet_osm_ways w,
                 neighborhood nb
            WHERE w.tags->>'highway' IN (
                'trunk', 'rest_area', 'track', 'bridleway', 'disused', 'service', 'secondary_link',
                'services', 'raceway', 'emergency_access_point', 'tertiary', 'primary', 'secondary',
                'tertiary_link', 'road', 'motorway', 'motorway_link', 'platform', 'construction',
                'corridor', 'primary_link', 'residential', 'trunk_link', 'bus_stop', 'trailhead',
                'living_street', 'unclassified', 'proposed'
            )
            AND ST_Intersects(
                ST_MakeLine(ARRAY(
                    SELECT ST_SetSRID(ST_MakePoint(n.lon / 1e7, n.lat / 1e7), 4326)
                    FROM unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality)
                    JOIN planet_osm_nodes n ON n.id = u.node_id
                    ORDER BY u.ordinality
                )),
                nb.geom
            )
        )
        SELECT
            rg.road_id,
            array_agg(n.id ORDER BY u.ordinality) AS node_ids,
            array_agg(n.lat / 1e7) AS node_lats,
            array_agg(n.lon / 1e7) AS node_lons,
            rg.oneway
        FROM road_geometries rg
        JOIN planet_osm_ways w ON rg.road_id = w.id
        JOIN LATERAL unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality) ON true
        JOIN planet_osm_nodes n ON n.id = u.node_id
        GROUP BY rg.road_id, rg.oneway;
        """
    )
    roads = cursor.fetchall()
    cursor.close()
    connection.close()
    return roads


# This function fetches all buildings from the postgres database that are inside the quarter.
# This is easier than importing the roads, since a node is either in or not in the area,
# so we can just say ST_Within instead of having to make a new object to also fetch the
# buildings that intersect the boundary (these do not exist).
def get_addresses(DB, neighborhood):
    connection = psycopg2.connect(dbname=DB, user=DB_USER, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        WITH neighborhood AS (
            SELECT ST_Transform(way, 4326) AS way
            FROM planet_osm_polygon
            WHERE place = 'quarter'
            AND name = '{neighborhood}'
        ),
        matched_nodes AS (
            SELECT
                n.id,
                n.lat / 1e7 AS lat,
                n.lon / 1e7 AS lon,
                n.tags->>'addr:city' AS city
            FROM
                planet_osm_nodes AS n,
                neighborhood AS nb
            WHERE
                n.tags->>'addr:postcode' IS NOT NULL
                AND ST_Within(
                    ST_SetSRID(ST_MakePoint(n.lon / 1e7, n.lat / 1e7), 4326),
                    nb.way
                )
        )
        SELECT * FROM matched_nodes;
        """
    )
    addresses = cursor.fetchall()
    cursor.close()
    connection.close()
    return addresses


# This function is not used. This function fetches the area of a quarter from the database,
# however this area overestimates the area that we need, since the quarters sometimes contain
# parks or lakes, or the buildings are only in a small part of the quarter. We need the area
# of the convex hull around the buildings, as calculated in area.py
def get_area(DB, neighborhood):
    connection = psycopg2.connect(dbname=DB, user=DB_USER, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        SELECT 
            p.way_area/1000000
        FROM 
            planet_osm_polygon as p 
        WHERE 
            place='quarter' 
        AND 
            name='{neighborhood}';
        """
    )
    area = cursor.fetchall()[0][0]
    cursor.close()
    connection.close()
    return area
