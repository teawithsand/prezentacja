{
  description = "Verixcel — render prezentacji (PDF/PPTX/demo)";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };

      python = pkgs.python3.withPackages (ps: [ ps.openpyxl ]);

      fonts = pkgs.makeFontsConf {
        fontDirectories = [ pkgs.ibm-plex pkgs.dejavu_fonts ];
      };

      runtime = pkgs.buildEnv {
        name = "verixcel-runtime";
        paths = [
          pkgs.marp-cli
          pkgs.chromium
          python
          pkgs.poppler_utils
          pkgs.ibm-plex
          pkgs.dejavu_fonts
          pkgs.bash
          pkgs.coreutils
        ];
      };

      render = pkgs.writeShellScriptBin "verixcel-render" ''
        export PATH="${runtime}/bin:$PATH"
        export CHROME_PATH="${pkgs.chromium}/bin/chromium"
        export FONTCONFIG_FILE="${fonts}"
        exec ${pkgs.bash}/bin/bash ./build.sh
      '';
    in
    {
      packages.${system}.default = render;

      apps.${system}.default = {
        type = "app";
        program = "${render}/bin/verixcel-render";
      };

      devShells.${system}.default = pkgs.mkShell {
        packages = [
          pkgs.marp-cli
          pkgs.chromium
          python
          pkgs.poppler_utils
          pkgs.ibm-plex
          pkgs.dejavu_fonts
        ];
      };
    };
}
