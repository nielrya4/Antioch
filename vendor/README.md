# vendor

Third-party code bundled so the CLI runs without pip or network access.

- `tomli` 2.2.1 (MIT, see `tomli/LICENSE`): TOML parser used only on Python < 3.11,
  which has no `tomllib`. `install.sh` and `antioch update` copy this directory beside `cli.py`.
