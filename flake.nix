{
  nixConfig = {
    extra-substituters = [
      "https://cache.nixos.org"
      "https://nix-community.cachix.org"
    ];
    extra-trusted-public-keys = [
      "cache.nixos.org-1:6NCHdD59X431o0gWypbMrAURkbJ16ZPMQFGspcDShjY="
      "nix-community.cachix.org-1:mB9FSh9qf2dCimDSUo8Zy7bkq5CX+/rkCWyvRCYg3Fs="
    ];
    allow-import-from-derivation = true;
    preferPrebuilt = true;
    accept-flake-config = true;
  };

  description = "Bill ETHBangkok Nix Flake";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
  };

  outputs = { self, nixpkgs, }:
    let
      allSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      forAllSystems = f:
        nixpkgs.lib.genAttrs allSystems
          (system: f {
            pkgs = import nixpkgs {
              inherit system;
              config = {
                allowUnfree = true;
                preferPrebuilt = true;
              };
            };
          });
    in
    {
      devShells = forAllSystems ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            python310
            poetry
            docker
            docker-compose
            nodejs_20
            yarn
            protobuf
            jq
          ];

          doCheck = false;

          shellHook = ''
            echo "Bill ETHBangkok Development Environment"
          '';
        };
      });
    };
}
