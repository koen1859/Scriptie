import psycopg2


# This function imports the roads from the database. It works as follows:
# we fetch a quarter from the polygon table, fetch all roads that satisfy a set of types
# and that are either: fully contained in the polygon, or partly in and partly outside of
# the polygon (i.e.  intersects the boundary). In this case we still fetch that entire road,
# also the parts that are not in the neighborhood. This is done because otherwise there are
# some edge cases where connections are missed that should have been there.
def get_road_data(DB, neighborhood):
    connection = psycopg2.connect(dbname=DB)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        -- First, get the neighborhood polygon, in the coordinate format we need.
        WITH neighborhood AS (
            SELECT ST_Transform(way, 4326) AS geom
            FROM planet_osm_polygon
            WHERE place = 'quarter'
              AND name = '{neighborhood}'
        ),
        -- Then, define the road geometries in a way that we can filter based 
        -- on whether they are inside the neighborhood.
        road_geometries AS (
            SELECT
                w.id AS road_id,
                w.nodes AS node_ids,
                w.tags->>'oneway' AS oneway,
                ST_MakeLine(ARRAY(
                    SELECT ST_SetSRID(ST_MakePoint(n.lon / 1e7, n.lat / 1e7), 4326)
                    FROM unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality)
                    JOIN planet_osm_nodes n ON n.id = u.node_id
                    ORDER BY u.ordinality
                )) AS road_geom
            FROM planet_osm_ways w
            -- Also filter based on the road type.
            WHERE w.tags->>'highway' IN (
                'trunk', 'rest_area', 'service', 'secondary_link',
                'services', 'tertiary', 'primary', 'secondary',
                'tertiary_link', 'road', 'motorway', 'motorway_link', 
                'corridor', 'primary_link', 'residential', 'trunk_link', 
                'living_street', 'unclassified', 'proposed'
            )
        ),
        -- Filter on whether the roads are at least partly in the neighborhood.
        filtered_roads AS (
            SELECT rg.*
            FROM road_geometries rg, neighborhood nb
            WHERE
                ST_Intersects(rg.road_geom, ST_Buffer(nb.geom, 0.001))
        )
        -- Select the attributes that are needed.
        SELECT
            fr.road_id,
            array_agg(n.id ORDER BY u.ordinality) AS node_ids,
            array_agg(n.lat / 1e7) AS node_lats,
            array_agg(n.lon / 1e7) AS node_lons,
            fr.oneway
        FROM filtered_roads fr
        JOIN planet_osm_ways w ON fr.road_id = w.id
        JOIN LATERAL unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality) ON true
        JOIN planet_osm_nodes n ON n.id = u.node_id
        GROUP BY fr.road_id, fr.oneway;
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
    connection = psycopg2.connect(dbname=DB)
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
    connection = psycopg2.connect(dbname=DB)
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


def get_features(DB, neighborhood):
    connection = psycopg2.connect(dbname=DB)
    cursor = connection.cursor()
    cursor.execute(
        f"""
        WITH neighborhood AS (
            SELECT ST_Transform(way, 4326) AS geom
            FROM planet_osm_polygon
            WHERE place = 'quarter'
            AND name = '{neighborhood}'
        ),
        natural_features AS (
            SELECT
                w.id,
                w.tags->>'natural' AS type,
                ST_MakeLine(ARRAY(
                    SELECT ST_SetSRID(ST_MakePoint(n.lon / 1e7, n.lat / 1e7), 4326)
                    FROM unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality)
                    JOIN planet_osm_nodes n ON n.id = u.node_id
                    ORDER BY u.ordinality
                )) AS geom
            FROM planet_osm_ways w
            WHERE w.tags->>'natural' IN (
                'scrub', 'wetland', 'sand', 'beach', 'strait', 'wood', 'shrubbery', 'ridge',
                'grassland', 'fell', 'valley', 'greenery', 'mud', 'scree', 'water', 'tree_row',
                'coastline', 'heath'
            )
        ),
        leisure AS (
            SELECT
                w.id,
                w.tags->>'leisure' AS type,
                ST_MakeLine(ARRAY(
                    SELECT ST_SetSRID(ST_MakePoint(n.lon / 1e7, n.lat / 1e7), 4326)
                    FROM unnest(w.nodes) WITH ORDINALITY AS u(node_id, ordinality)
                    JOIN planet_osm_nodes n ON n.id = u.node_id
                    ORDER BY u.ordinality
                )) AS geom
            FROM planet_osm_ways w
            WHERE w.tags->>'leisure' IN (
                'fishing', 'fitness_centre', 'outdoor_seating', 'golf_course', 'sports_centre',
                'garden', 'swimming_pool', 'sauna', 'track', 'miniature_train', 'nature_reserve',
                'bandstand', 'slipway', 'resort', 'stadium', 'marina', 'practice_pitch',
                'water_park', 'horse_riding', 'firepit', 'park;playground', 'schoolyard',
                'bleachers', 'recreation_ground', 'bird_hide', 'ice_rink', 'amusement_arcade',
                'pitch', 'miniature_golf', 'swimming_area', 'playground', 'park',
                'fitness_station', 'sports_hall', 'dog_park'
            )
        ),
        features AS (
            SELECT * FROM natural_features
            UNION ALL
            SELECT * FROM leisure
        ),
        filtered_features AS (
            SELECT f.*
            FROM features f, neighborhood nb
            WHERE
                ST_Intersects(f.geom, nb.geom)
        )
        SELECT type, COUNT(*) AS count
        FROM filtered_features
        GROUP BY type
        ORDER BY count DESC;
        """
    )
    features = cursor.fetchall()
    cursor.close()
    connection.close()
    return features
