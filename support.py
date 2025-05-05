from os import walk
import pygame
import os
from settings import sc
import re

def import_folder(path):
    surface_list = []

    valid_extensions = ['.png', '.jpg', '.jpeg']

    for _, __, img_files in walk(path):
        img_files.sort(key=lambda f: [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', f)])
        for image in img_files:
            # Skip hidden files (like .DS_Store) and non-image files
            if image.startswith('.') or not os.path.splitext(image)[1].lower() in valid_extensions:
                continue

            full_path = os.path.join(path, image)
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                new_width = int(image_surf.get_width() * sc)
                new_height = int(image_surf.get_height() * sc)
                image_surf = pygame.transform.scale(image_surf, (new_width, new_height))
                surface_list.append(image_surf)
            except pygame.error as e:
                print(f"Error loading {full_path}: {e}")

    return surface_list

def import_folder_without_sc(path):
    surface_list = []

    valid_extensions = ['.png', '.jpg', '.jpeg']

    for _, __, img_files in walk(path):
        img_files.sort(key=lambda f: [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', f)])
        for image in img_files:
            # Skip hidden files (like .DS_Store) and non-image files
            if image.startswith('.') or not os.path.splitext(image)[1].lower() in valid_extensions:
                continue

            full_path = os.path.join(path, image)
            try:
                image_surf = pygame.image.load(full_path).convert_alpha()
                surface_list.append(image_surf)
            except pygame.error as e:
                print(f"Error loading {full_path}: {e}")

    return surface_list