{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = [
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
