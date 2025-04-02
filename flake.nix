{
  description = "Nix shell with Python and ML dependencies";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }: 
  let 
    pkgs = nixpkgs.legacyPackages.x86_64-linux;
    python = pkgs.python312;
  in {
    devShells.x86_64-linux.default = pkgs.mkShell {
      packages = [
        python
        (python.withPackages (ps: with ps; [
          numpy
          pandas
          joblib
          flask
          scikit-learn
          gunicorn
        ]))
      ];
    };
  };
}
