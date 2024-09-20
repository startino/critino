{ pkgs ? import <nixpkgs> {} }:
(pkgs.buildFHSUserEnv {
    name = "pipzone";
    targetPkgs = pkgs: (with pkgs; [
        python312
        poetry
        nixpacks
    ]);
    runScript = "fish";
}).env
