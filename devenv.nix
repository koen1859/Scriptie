{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = with pkgs; [
    (python3.withPackages (ps:
      with ps; [
        igraph
        psycopg2
        shapely
        numpy
        matplotlib
        folium
        ujson
        geopandas
      ]))
    postgresql_17
    postgresql17Packages.postgis
    osm2pgsql
    (pkgs.callPackage ./lkh.nix {}) # The Lin-Kernighan heuristic (we fetch this from lkh.nix, the other nix file in the repo)
    (import ./initdb.nix {inherit pkgs;})
  ];

  services.postgres = {
    enable = true;
    package = pkgs.postgresql_17;
    extensions = extensions:
      with extensions; [
        postgis
      ];
  };
}
