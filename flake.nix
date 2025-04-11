{
  description = "Dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
      };
      python-env = pkgs.python3.withPackages (ps:
        with ps; [
          igraph
          psycopg2
          shapely
          numpy
          matplotlib
          folium
        ]);
      pg = pkgs.postgresql_17;
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          python-env
          pkgs.osm2pgsql
          pkgs.gdal
          pkgs.postgis
          pkgs.postgresql_17
          pkgs.postgresql17Packages.postgis
          (pkgs.callPackage ./lkh.nix {})
        ];

        shellHook = ''
          export PGDATA=$PWD/.pgdata
          export PGPORT=5433
          export PATH="$PGDATA/bin:$PATH"

          if [ ! -d "$PGDATA" ]; then
            ${pg}/bin/initdb -D "$PGDATA"
            echo "local all all trust" > "$PGDATA/pg_hba.conf"
            echo "host all all 127.0.0.1/32 trust" >> "$PGDATA/pg_hba.conf"
            echo "host all all ::1/128 trust" >> "$PGDATA/pg_hba.conf"
          fi
          ${pg}/bin/pg_ctl -D "$PGDATA" -o "-p $PGPORT" -l "$PGDATA/logfile" start
        '';
      };
    });
}
