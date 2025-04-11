#!/bin/bash

export PGUSER="postgres"
export PGHOST="localhost"
export PGPORT="5432"

for file in data/*.osm.pbf; do
	# Extract base name
	base=$(basename "$file" -latest.osm.pbf)

	# Replace hyphens with underscores
	dbname=${base//-/_}

	echo "Creating database: $dbname"
	sudo -u postgres psql -c "DROP DATABASE IF EXISTS $dbname;"
	sudo -u postgres psql -c "CREATE DATABASE $dbname;"

	echo "Enabling extensions on $dbname"
	sudo -u postgres psql -d "$dbname" -c "CREATE EXTENSION postgis;"
	sudo -u postgres psql -d "$dbname" -c "CREATE EXTENSION hstore;"

	echo "Importing data from $file into $dbname"
	osm2pgsql --create --hstore --slim --multi-geometry --database "$dbname" "$file"
done
