Maps generated with this code are on [www.koenstevens.nl/?page_id=182](https://koenstevens.nl/?page_id=182)

```{nix}
postgresql = {
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
```
