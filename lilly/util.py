"""
Module containing utility functions common to all sections of lilly
"""
import os


def get_folders(parent_dir: str):
    """Returns all the folders in a given parent folder"""
    for it in os.scandir(parent_dir):
        if it.is_dir():
            print(it.path)
