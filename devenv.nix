{
  pkgs,
  lib,
  config,
  inputs,
  ...
}: {
  packages = [
    pkgs.git
    pkgs.pyright
    pkgs.ruff
  ];

  languages.python = {
    enable = true;
    lsp.enable = true;
    uv.enable = true;
  };

  git-hooks.hooks = {
    action-validator.enable = true;
    actionlint.enable = true;
    check-python.enable = true;
    check-toml.enable = true;
    pyright.enable = true;
    ruff.enable = true;
    ruff-format.enable = true;
    uv-check.enable = true;
  };
}
