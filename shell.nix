with import <nixpkgs> { };

mkShell {
  NIX_LD_LIBRARY_PATH = lib.makeLibraryPath [
    gcc-unwrapped.lib
  ];
  NIX_LD = lib.fileContents "${stdenv.cc}/nix-support/dynamic-linker";
}
