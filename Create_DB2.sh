#!/bin/bash
export PGUSER="postgres"
export PGHOST="localhost"
export PGPORT="5432"

# osm2pgsql --create --hstore --multi-geometry --database groningen_data nodes_roads_buildings.osm.pbf
osm2pgsql --create --hstore --slim --multi-geometry --database groningen_data groningen-latest.osm.pbf
