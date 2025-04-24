{
  description = "thesis shell";

  inputs = {
    # Declare the source for the Nix packages
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # Some useful functions
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
  }:
  # Create a dev shell, supported on linux and macos.
    flake-utils.lib.eachDefaultSystem (system: let
      # Load the package set for the current system (i.e. x86_64-linux)
      pkgs = nixpkgs.legacyPackages.${system};

      # Declare the python packages that are needed
      python-env = pkgs.python3.withPackages (ps:
        with ps; [
          igraph
          psycopg2
          shapely
          numpy
          matplotlib
          folium
          ujson
          geopandas
        ]);
    in {
      # Define the development shell
      devShells.default = pkgs.mkShell {
        buildInputs = [
          python-env # The previously defined python env
          pkgs.osm2pgsql # To load .osm.pbf data to postgresql database
          (pkgs.callPackage ./lkh.nix {}) # The Lin-Kernighan heuristic (we fetch this from lkh.nix, the other nix file in the repo)
        ];

        # I use zsh shell, so i start it, the default is bash.
        # If you want to use bash shell, comment out this part.
        shellHook = ''
          export SHELL=${pkgs.zsh}/bin/zsh
          exec ${pkgs.zsh}/bin/zsh
        '';
      };
    });
}
