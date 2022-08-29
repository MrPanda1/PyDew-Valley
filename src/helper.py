import pygame
from os import walk

def import_folder(path: str) -> list:
    """
    Import all surfaces in a folder.
    """
    surface_list = []

    for _, _, files in walk(path):
        for file in files:
            surface_list.append(pygame.image.load(path + '/' + file).convert_alpha())

    return surface_list