{ pkgs ? import <nixpkgs> {} }:

let
  fonts = pkgs.makeFontsConf {
    fontDirectories = [
      pkgs.ibm-plex
      pkgs.dejavu_fonts
    ];
  };
in
pkgs.mkShell {
  packages = [
    pkgs.nodejs_20
    pkgs.chromium
    (pkgs.python3.withPackages (ps: [ ps.openpyxl ]))
    pkgs.poppler_utils
    pkgs.ibm-plex
    pkgs.dejavu_fonts
  ];

  CHROME_PATH = "${pkgs.chromium}/bin/chromium";
  FONTCONFIG_FILE = "${fonts}";

  shellHook = ''
    echo "verixcel env: node $(node -v), python $(python3 --version | cut -d' ' -f2), chromium ready"
  '';
}