#!/bin/bash

export PGUSER="koenstevens"

for file in data/*.osm.pbf; do
	# Extract base name
	base=$(basename "$file" -latest.osm.pbf)

	# Replace hyphens with underscores
	dbname=${base//-/_}

	echo "Creating database: $dbname"
	psql -c "DROP DATABASE IF EXISTS $dbname;"
	psql -c "CREATE DATABASE $dbname;"

	echo "Enabling extensions on $dbname"
	psql -d "$dbname" -c "CREATE EXTENSION postgis;"
	psql -d "$dbname" -c "CREATE EXTENSION hstore;"

	echo "Importing data from $file into $dbname"
	osm2pgsql --create --hstore --slim --multi-geometry --database "$dbname" "$file"
done
