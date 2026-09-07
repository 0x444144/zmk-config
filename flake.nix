{
  description = "ZMK firmware dev env for the cradio/Sweep (nice!nano v2)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = f:
        nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          # The Zephyr SDK is not in nixpkgs, and ZMK is very particular about
          # its toolchain version, so the compiler lives in the official
          # zmk-build-arm container. Everything here is host-side glue.
          packages = with pkgs; [
            keymap-drawer # `zmk draw` -> keymap.svg
            util-linux # lsblk, for finding the NICENANO volume
            udisks # mounting it without root
            dfu-util
            git
          ];

          shellHook = ''
            export PATH="$PWD/dev:$PATH"
            if ! command -v docker >/dev/null; then
              echo "warning: docker not on PATH -- enable virtualisation.docker in your NixOS config"
            fi
            echo "zmk-config dev shell -- run 'zmk help'"
          '';
        };
      });

      formatter = forAllSystems (pkgs: pkgs.nixpkgs-fmt);
    };
}
