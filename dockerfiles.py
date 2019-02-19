import requests
from pathlib import Path
import click
from glob import glob
from subprocess import run


@click.group()
def main():
    """Dockerfile tool."""


@main.command()
def build():

    for dockerfile in sorted(glob("./*/**/Dockerfile") + glob("./*/Dockerfile")):

        tag_name = Path(dockerfile).parent.name

        run(
            [
                "docker",
                "build",
                Path(dockerfile).parent,
                "-t",
                f"python-poetry:{tag_name}",
            ]
        )


@main.command()
def clean():
    for dockerfile in sorted(glob("./*/**/Dockerfile") + glob("./*/Dockerfile")):

        path = Path(dockerfile)
        path.unlink()
        path.parent.rmdir()
        try:
            if int(path.name[0]):
                path.parent.parent.rmdir()
        except ValueError:
            pass


@main.command()
@click.option("-v", "--poetry-version", default="master", type=str)
def make(poetry_version="master"):
    """Generate docker files for all tags."""
    tags = requests.get(
        "https://registry.hub.docker.com/v1/repositories/python/tags"
    ).json()

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
