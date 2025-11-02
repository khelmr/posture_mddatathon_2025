{
  description = "Develop Python on Nix with uv";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };

  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
      
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = import nixpkgs {
            system = "${system}";
            config = {
              allowUnfree = true;
              cudaSupport = true;
            };
          };
          nvidiaPackage = pkgs.linuxPackages.nvidiaPackages.stable;
        in
          {
            formatter."${system}" = nixpkgs.legacyPackages.${system}.alejandra;
            default = pkgs.mkShell {
              packages = with pkgs; [
                python3
                uv
                ffmpeg
                fmt.dev
                cudaPackages.cuda_cudart
                cudatoolkit
                cudaPackages.cudnn
                libGLU
                libGL
                xorg.libXi
                xorg.libXmu
                freeglut
                xorg.libXext
                xorg.libX11
                xorg.libXv
                xorg.libXrandr
                zlib
                ncurses
                stdenv.cc
                binutils
              ];

              shellHook = ''
                unset PYTHONPATH
              export LD_LIBRARY_PATH="${nvidiaPackage}/lib:$LD_LIBRARY_PATH"
        export CUDA_PATH=${pkgs.cudatoolkit}
        export EXTRA_LDFLAGS="-L/lib -L${nvidiaPackage}/lib"
        export EXTRA_CCFLAGS="-I/usr/include"
        export CMAKE_PREFIX_PATH="${pkgs.fmt.dev}:$CMAKE_PREFIX_PATH"
        export PKG_CONFIG_PATH="${pkgs.fmt.dev}/lib/pkgconfig:$PKG_CONFIG_PATH"
              uv sync
              . .venv/bin/activate
              '';
            };
          }
      );
    };
}
