#!/bin/bash

# Install the required packages
# yay -S osmium-tool osm2pgswl postgresql postgis

# Look at the data
osmium fileinfo groningen-latest.osm.pbf
# osmium tags-count groningen-latest.osm.pbf
# osmium tags-count groningen-latest.osm.pbf | grep road
# osmium tags-count groningen-latest.osm.pbf | grep highway

# Keep only the roads and buildings
osmium tags-filter groningen-latest.osm.pbf nw/highway w/building a/building -o roads_buildings.osm.pbf --overwrite

# Look at the new data
# osmium fileinfo roads_buildings.osm.pbf
# osmium tags-count roads_buildings.osm.pbf | grep highway
# osmium tags-count roads_buildings.osm.pbf | grep building

# Add the nodes to this data
osmium add-locations-to-ways -o nodes_roads_buildings.osm.pbf roads_buildings.osm.pbf --overwrite

# Look at the final data
osmium fileinfo nodes_roads_buildings.osm.pbf
