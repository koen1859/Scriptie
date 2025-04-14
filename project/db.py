import psycopg2
from config import DB_HOST, DB_NAME, DB_PORT, DB_USER


def get_road_data():
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()
    cursor.execute(
        """
    WITH neighborhood_boundary_ways AS (
    SELECT (member->>'ref')::bigint AS way_id
    FROM planet_osm_rels AS r
    CROSS JOIN LATERAL jsonb_array_elements(r.members) AS member
    WHERE r.tags->>'place' = 'quarter'
    AND r.tags->>'name' = 'Oosterpoort'
    AND member->>'role' = 'outer'
    AND member->>'type' = 'W'
),
boundary_geometries AS (
    SELECT
        w.id AS way_id,
        ST_MakeLine(
            ARRAY(
                SELECT ST_SetSRID(ST_MakePoint(n.lon/1e7, n.lat/1e7), 4326)
                FROM unnest(w.nodes) WITH ORDINALITY AS node_id
                JOIN planet_osm_nodes AS n ON n.id = node_id.node_id
                ORDER BY ordinality
            )
        ) AS geom
    FROM planet_osm_ways AS w
    JOIN neighborhood_boundary_ways ON w.id = way_id
),
neighborhood_polygon AS (
    SELECT ST_BuildArea(ST_Collect(geom)) AS geom
    FROM boundary_geometries
),
road_geometries AS (
    SELECT
        w.id AS road_id,
        ST_MakeLine(
            ARRAY(
                SELECT ST_SetSRID(ST_MakePoint(n.lon/1e7, n.lat/1e7), 4326)
                FROM unnest(w.nodes) WITH ORDINALITY AS node_id
                JOIN planet_osm_nodes AS n ON n.id = node_id.node_id
                ORDER BY ordinality
            )
        ) AS geom
    FROM planet_osm_ways AS w
    WHERE w.tags->>'highway' IN (
        'motorway', 'trunk', 'primary', 'secondary', 'tertiary',
        'unclassified', 'residential', 'living_street', 'motorway_link', 'trunk_link',
        'primary_link', 'secondary_link', 'tertiary_link'
    )
)
SELECT
    w.id AS road_id,
    array_agg(n.id ORDER BY u.ordinality) AS node_ids,
    array_agg(n.lat / 1e7) AS node_lats,
    array_agg(n.lon / 1e7) AS node_lons,
    w.tags->>'oneway' AS oneway
FROM road_geometries rg
JOIN planet_osm_ways w ON rg.road_id = w.id
JOIN LATERAL unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality) ON true
JOIN planet_osm_nodes n ON n.id = u.node_id
CROSS JOIN neighborhood_polygon np
WHERE ST_Within(rg.geom, np.geom)
GROUP BY w.id, w.tags->>'oneway';"""
    )
    roads = cursor.fetchall()
    cursor.close()
    connection.close()
    return roads


def get_addresses():
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()
    cursor.execute(
        """
        WITH neighborhood_boundary_ways AS (
            SELECT (member->>'ref')::bigint AS way_id
            FROM planet_osm_rels AS r
            CROSS JOIN LATERAL jsonb_array_elements(r.members) AS member
            WHERE r.tags->>'place' = 'quarter'
            AND r.tags->>'name' = 'Oosterpoort'
            AND member->>'role' = 'outer'
            AND member->>'type' = 'W'
        ),
        boundary_geometries AS (
            SELECT
                w.id AS way_id,
                ST_MakeLine(
                    ARRAY(
                        SELECT ST_SetSRID(ST_MakePoint(n.lon/1e7, n.lat/1e7), 4326)
                        FROM unnest(w.nodes) WITH ORDINALITY AS node_id
                        JOIN planet_osm_nodes AS n ON n.id = node_id.node_id
                        ORDER BY ordinality
                    )
                ) AS geom
            FROM planet_osm_ways AS w
            JOIN neighborhood_boundary_ways ON w.id = way_id
        ),
        neighborhood_polygon AS (
            SELECT ST_BuildArea(ST_Collect(geom)) AS geom
            FROM boundary_geometries
        )
        SELECT 
            n.id, 
            n.lat / 1e7 AS lat, 
            n.lon / 1e7 AS lon, 
            n.tags->>'addr:city' AS city
        FROM 
            planet_osm_nodes AS n
        JOIN neighborhood_polygon np ON ST_Within(
            ST_SetSRID(ST_MakePoint(n.lon/1e7, n.lat/1e7), 4326),
            np.geom
        )
        WHERE 
            n.tags->>'addr:postcode' IS NOT NULL;
    """
    )
    addresses = cursor.fetchall()
    cursor.close()
    connection.close()
    return addresses
