In order to run this project you need to have the `postgres` service, with the `postgis` extension
set up on your system, below is how I did it on my system as an example (using `nix`):
```nix
{pkgs, ...}: {
    services.postgresql = {
      enable = true;
      package = pkgs.postgresql_17;
      dataDir = "/var/lib/postgresql/data";
      extensions = with pkgs.postgresql17Packages; [postgis];
      authentication = ''
        local   all             all                                     trust
        host    all             all             127.0.0.1/32            trust
        host    all             all             ::1/128                 trust
      '';
    };
}
```
You need to create a directory called `data`, and store the .osm.pbf files from Groningen and
Noord-Holland in there. These files can be downloaded from here: 
https://download.geofabrik.de/europe/netherlands.html. If you use Nix package manager and have 
flakes enabled, you can just run `nix develop` when you are inside the directory and it will 
download all dependencies. Otherwise, all dependencies are listed in the `flake.nix` file, they 
can also be downloaded manually. First, run the `Create_DB.sh` script. This will create the 
`postgres` databases for all provinces. Then, move into the `project` directory and run 
`python main.py` and the entire project will run. But, the already generated TSPs (and their solutions)
are included in the repository already. You can also use the `testing.py` file to make some
visualisations and print results for a specific area.
