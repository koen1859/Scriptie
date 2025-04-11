{
  description = "Dev shell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
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
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = [
          python-env
          pkgs.osm2pgsql
          (pkgs.callPackage ./lkh.nix {})
        ];
      };
    });
}
