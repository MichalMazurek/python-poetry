# Python & Poetry

Python Docker Images with Poetry for you.

- Python <https://www.python.org>
- Poetry <https://poetry.eustace.io>

The goal of this project is to easily build and push python&poetry images to docker registry so you can use it in your CI/CD to build packages.

## Installation

```bash
make install
```

> you need latest version of Poetry install <https://poetry.eustace.io>

## Make & Build

```bash
make all TAGS
```

Example:

```bash
make all latest 3.6 3.7
```

This will make images for python:latest, python:3.6, python:3.7.

## Push to docker registry

```bash
make push {docker-registry or username in docker hub}
```

Example:

```bash
make push michalmazurek
```

This will push all built images to docker registry (with example above, to: michalmazurek/python-poetry:{TAG})

```bash
make push hub.example.com/user
```

This will push images to hub.example.com/user/python-poetry:{tag}

> You can find currently built tags in `./tags.txt`.

## Command Line Interface

`--help` it for more info.

```bash
Usage: dockerfiles.py [OPTIONS] COMMAND [ARGS]...

  Dockerfile tool.

Options:
  --help  Show this message and exit.

Commands:
  build  Build docker images.
  clean
  make   Generate docker files for all tags.
  push   Push docker images.
```
