"""The script that is run to do any management tasks like creating the app or the service"""
import os
import shutil
from typing import List

import click

STUBS_FOLDER_PATH = os.path.join(os.path.dirname(__file__), "stubs")


@click.group()
def cli():
    pass


@click.command()
@click.option("--folder-path", default="./services", help="path to the folder that should contain services")
@click.argument("name")
def create_service(name: str, folder_path: str = "./services"):
    """Creates the whole folder required for a given service"""
    click.echo("Sit back as we create your service")
    _create_sample_service(name, folder_path=folder_path)
    click.echo(f"Service {name} created in the {folder_path} folder")


@click.command()
def create_app():
    """Creates a beginner app in the current folder"""
    root_folder = os.path.abspath(".")
    _copy_stub_file(dst=root_folder, file_name="settings.py")
    _copy_stub_file(dst=root_folder, file_name="main.py")
    _create_sample_service("hello")


def _create_sample_service(name: str, folder_path: str = "./services"):
    """This creates a sample service of the given name and puts it in the given folder path"""
    service_os_path = os.path.join(folder_path, name)
    os.makedirs(service_os_path)
    _copy_stub_service_to_folder(service_os_path)


def _copy_stub_file(dst: str, file_name: str):
    """Copies a stub file from the stubs folder to the destination folder"""
    stub_file = os.path.join(STUBS_FOLDER_PATH, file_name)
    new_file_path = os.path.join(dst, file_name)
    shutil.copyfile(stub_file, new_file_path)


def _copy_stub_service_to_folder(dst: str):
    """Copies the stub service to the folder path (dst) provided"""
    stub_service_folder_path = os.path.join(STUBS_FOLDER_PATH, "service")
    stub_service_files = _get_files_in_folder(parent_dir=stub_service_folder_path)
    for file in stub_service_files:
        new_file_path = os.path.join(dst, file.name)
        shutil.copyfile(file.path, new_file_path)


def _get_files_in_folder(parent_dir: str) -> List[os.DirEntry]:
    """Returns all the files in a given parent folder"""
    return [file for file in os.scandir(parent_dir) if file.is_file(follow_symlinks=False)]  # noqa


if __name__ == '__main__':
    cli.add_command(create_service)
    cli.add_command(create_app)
    cli()
