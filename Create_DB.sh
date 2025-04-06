#!/bin/bash

sudo -u postgres psql -c "CREATE DATABASE groningen_data;"
sudo -u postgres psql -d groningen_data -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d groningen_data -c "CREATE EXTENSION hstore"

export PGUSER="postgres"
export PGHOST="localhost"
export PGPORT="5432"

osm2pgsql --create --hstore --slim --multi-geometry --database groningen_data groningen-latest.osm.pbf
