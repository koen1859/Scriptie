{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = [
    pkgs.osm2pgsql
    (pkgs.callPackage ./lkh.nix {})
    (pkgs.python3.withPackages (ps:
      with ps; [
        igraph
        psycopg2
        shapely
        numpy
        matplotlib
        folium
      ]))
  ];
}
