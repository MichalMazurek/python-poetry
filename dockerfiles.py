import requests
from pathlib import Path
import click
from glob import glob
from subprocess import run
import fnmatch
from functools import partial


@click.group()
def main():
    """Dockerfile tool."""


@main.command()
def build():
    """Build docker images."""
    tags = []
    for dockerfile in sorted(glob("./*/**/Dockerfile") + glob("./*/Dockerfile")):

        tag_name = Path(dockerfile).parent.name
        tags.append(tag_name)
        run(
            [
                "docker",
                "build",
                Path(dockerfile).parent,
                "-t",
                f"python-poetry:{tag_name}",
            ]
        )

    Path("./tags.txt").write_text("\n".join(tags))


@main.command()
@click.argument("docker_hub_prefix", nargs=1)
def push(docker_hub_prefix: str):
    """Push docker images."""

    prefix = (
        docker_hub_prefix + "/python-poetry" if docker_hub_prefix else "python-poetry"
    )
    for tag in Path("./tags.txt").read_text("utf8").splitlines():

        run(["docker", "tag", f"python-poetry:{tag}", f"{prefix}:{tag}"])
        run(["docker", "push", f"{prefix}:{tag}"])


@main.command()
def clean():
    for dockerfile in sorted(glob("./*/**/Dockerfile") + glob("./*/Dockerfile")):

        path = Path(dockerfile)
        path.unlink()
        path.parent.rmdir()
        try:
            if int(path.parent.name[0]):
                path.parent.parent.rmdir()
        except (ValueError, OSError):
            pass


@main.command()
@click.argument("tag_masks", nargs=-1)
@click.option("-v", "--poetry-version", default="master", type=str)
def make(tag_masks: str = "*", poetry_version: str = "master"):
    """Generate docker files for all tags."""
    tags = requests.get(
        "https://registry.hub.docker.com/v1/repositories/python/tags"
    ).json()

    def match_tag(tag) -> bool:
        tag_name = tag["name"]
        return [
            tag_mask
            for tag_mask in tag_masks
            if tag_mask == "*" or fnmatch.fnmatch(tag_name, tag_mask)
        ]

    tags = list(filter(match_tag, tags))

    click.echo(f"Found {len(tags)} tags.")
    click.echo("Generating ", nl=False)

    docker_3_template = Path("./Dockerfile-3.template").read_text("utf8")
    docker_2_template = Path("./Dockerfile-2.template").read_text("utf8")

    for tag in tags:
        tag_name = tag["name"]

        docker_template = docker_3_template

        try:
            tag_major_version = int(tag_name[0])
            tag_major_path = Path(str(tag_major_version))
            try:
                tag_major_path.mkdir()
            except FileExistsError:
                pass
            tag_path = tag_major_path / Path(tag_name)
            if tag_major_version == 2:
                docker_template = docker_2_template
        except ValueError:
            tag_path = Path(tag_name)

        try:
            tag_path.mkdir()
        except FileExistsError:
            pass

        (tag_path / "Dockerfile").write_text(
            docker_template.format(python_tag=tag_name, poetry_version=poetry_version)
        )
        click.echo(".", nl=False)
    click.echo(" Done.")


if __name__ == "__main__":

    main()
