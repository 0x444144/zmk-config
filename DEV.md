# Local dev environment

Builds this keymap on your own machine instead of waiting on GitHub Actions.
The Zephyr SDK isn't packaged in nixpkgs and ZMK is fussy about its exact
toolchain version, so the compiler comes from the official
`zmkfirmware/zmk-build-arm` container — the same one CI uses. The Nix flake
supplies the host-side glue (helper script, keymap-drawer, flashing tools).

## Requirements

Docker, and your user in the `docker` group. On NixOS:

```nix
virtualisation.docker.enable = true;
users.users.<you>.extraGroups = [ "docker" ];
```

## Use

```console
$ cd ~/dev/projects/zmk-config
$ nix develop          # or: direnv allow
$ zmk init             # once: pulls the image + clones the west workspace
$ zmk build            # both halves -> firmware/cradio_{left,right}.uf2
$ zmk flash left       # double-tap reset on the half, then it copies the .uf2
```

`zmk help` lists everything. `zmk build left` builds one half; `zmk draw`
renders the keymap to `.build/keymap.svg`; `ZMK_PRISTINE=1 zmk build` forces a
clean rebuild.

## Notes

- `zmk init` clones ~3.5 GB into `.build/` (gitignored; Zephyr pulls in a lot of HAL modules this board never uses). Only needs redoing when
  the pinned ZMK revision in `config/west.yml` changes — rerun `zmk init` then.
- Incremental builds are fast; edits to `config/*.keymap` or `config/*.conf`
  rebuild in seconds. Adding or removing a `.c` file needs `ZMK_PRISTINE=1`.
- The ZMK revision always comes from `config/west.yml`, so local builds and the
  GitHub Actions build stay in sync.
- `firmware/` and `.build/` are gitignored; CI is still the source of truth for
  release artifacts.
