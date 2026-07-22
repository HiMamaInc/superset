This directory holds the Lillio-owned downstream layer on top of upstream Superset.

Contents:
- `docker/`: image overlay and production config files.
- root `.circleci/config.yml`: branch-only CI for building and deploying the Lillio image.

`master` is intended to stay identical to upstream. `lillio-master` carries this overlay layer.