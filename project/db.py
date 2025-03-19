import psycopg2
from config import DB_HOST, DB_NAME, DB_PORT, DB_USER


def get_road_data():
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            w.id AS road_id,
            array_agg(n.id ORDER BY u.ordinality) AS node_ids,
            array_agg(n.lat / 10^7 ) AS node_lats,
            array_agg(n.lon / 10^7 ) AS node_lons,
            w.tags->>'oneway' AS oneway
        FROM
            planet_osm_ways AS w
        JOIN
            LATERAL unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality)
            ON true
        JOIN
            planet_osm_nodes AS n
            ON n.id = u.node_id
        WHERE
            w.tags->>'highway' IN (
                'motorway', 'trunk', 'primary', 'secondary', 'tertiary',
                'unclassified', 'residential', 'motorway_link', 'trunk_link',
                'primary_link', 'secondary_link', 'tertiary_link'
            )
        GROUP BY
            w.id;
    """)
    roads = cursor.fetchall()
    cursor.close()
    connection.close()
    return roads


def get_addresses():
    connection = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, host=DB_HOST, port=DB_PORT
    )
    cursor = connection.cursor()
    cursor.execute("""
        SELECT n.id, n.lat / 10^7, n.lon / 10^7
        FROM planet_osm_nodes AS n
        WHERE n.tags ->> 'addr:postcode' IS NOT NULL;
    """)
    addresses = cursor.fetchall()
    cursor.close()
    connection.close()
    return addresses
