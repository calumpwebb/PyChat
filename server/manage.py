# TODO: find a way to share this file between client and server
import os

import click

from src import config, db


def run_commands(commands, args):
    for command in commands:
        command_to_exec = command.format(*args)
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
        commands += ["docker build -f docker/{0} -t {1} . "]

    if push:
        commands += ["docker push {1}"]

    docker_args = "{}/{}:{}".format(user, repo, tag)

    run_commands(commands, (repo, docker_args))


"""
User Management
"""


@cli.command()
@click.option("-u", "--username", type=str, required=True)
@click.option("-p", "--password", type=str, required=True)
def add_user(username, password):
    session = config.get_session()

    session.add(db.User(username=username, password=password))

    session.commit()


if __name__ == "__main__":
    cli()
