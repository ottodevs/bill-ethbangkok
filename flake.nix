{
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
          (system: f { pkgs = import nixpkgs { inherit system; }; });
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

          shellHook = ''
            echo "Bill ETHBangkok Development Environment"
          '';
        };
      });
    };
}
