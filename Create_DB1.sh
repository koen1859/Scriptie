#!/bin/bash

# Install the dependencies
# yay -S postgresql postgis osm2pgsql

# Initialize database
# sudo su -l postgres -c "initdb --locale=C.UTF-8 --encoding=UTF8 -D '/var/lib/postgres/data'"

# Start and enable systemd service
# sudo systemctl start postgresql
# sudo systemctl enable postgresql

# Create the groningen database and add the extensions
sudo -u postgres psql -c "CREATE DATABASE groningen_data;"
sudo -u postgres psql -d groningen_data -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d groningen_data -c "CREATE EXTENSION hstore"

# Now the database should be ready to be filled with the OSM data
