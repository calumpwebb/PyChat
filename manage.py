import os

import click


def run_commands(commands, args):
    for command in commands:
        command_to_exec = command.format(args)
        print("Running", command_to_exec)
        os.system(command_to_exec)
        print("")


@click.group()
def cli():
    pass


@cli.command()
@click.option("-f", "--file-path", type=str, default=".")
def clean(file_path):
    commands = ["black {}", "isort -rc {}"]

    run_commands(commands, file_path)


@cli.command()
@click.option("-t", "--tag", type=str, default="latest")
@click.option("-b", "--build", type=bool, default=True)
@click.option("-p", "--push", type=bool, default=True)
@click.option("-u", "--user", type=str, required=True)
@click.option("-r", "--repo", type=str, required=True)
def docker(tag, build, push, user, repo):
    commands = []

    if build:
        commands += ["docker build -t {} ."]

    if push:
        commands += ["docker push {}"]

    docker_args = "{}/{}:{}".format(user, repo, tag)

    run_commands(commands, docker_args)


if __name__ == "__main__":
    cli()
