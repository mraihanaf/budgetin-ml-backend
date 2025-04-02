{
  description = "Flask API with Machine Learning Dependencies";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: 
  let 
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      buildInputs = [
        pkgs.python312
        pkgs.python312Packages.pip
        pkgs.python312Packages.virtualenv
      ];

      shellHook = ''
        if [ ! -d ".venv" ]; then
          virtualenv .venv
        fi
        source .venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
      '';
    };
  };
}
