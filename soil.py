import pygame
from settings import *
from support import import_folder

from abc import ABC, abstractmethod

class Growable(ABC):
    @abstractmethod
    def grow(self): pass

class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft  = pos)
        self.z = LAYERS['soil']

class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil water']

class Plant(pygame.sprite.Sprite, Growable):
    def __init__(self, plant_type, groups, soil, check_watered):
        super().__init__(groups)
        self.plant_type = plant_type
        self.frames = import_folder(f'images/soil/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered

        #plant grow
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = 1
        self.harvestable = False

        #setup
        self.image = self.frames[self.age]
        self.rect = self.image.get_rect(topleft = soil.rect.topleft)
        self.z = LAYERS['ground plant']

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            if int(self.age) > 0:
                self.z = LAYERS['main']

            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvestable = True

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(topleft = self.soil.rect.topleft)


class SoilLayer:
    def __init__(self, all_sprites, tree_sprites):

        #sprite groups
        self.all_sprites = all_sprites
        self.tree_sprites = tree_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        #gr
        self.soil_surf = pygame.image.load('images/soil/soil.png')

        self.create_soil_grid()
        self.create_hit_rects()

    def create_soil_grid(self):
        ground = pygame.image.load('images/layers/world.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(int(h_tiles))] for row in range(int(v_tiles))]
        for x, y in farmable_pos:
            self.grid[y][x].append('F')
        #print(self.grid)

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = int(rect.x // TILE_SIZE)
                y = int(rect.y // TILE_SIZE)

                has_tree = False
                for tree in self.tree_sprites.sprites():
                    if tree.rect.collidepoint(point):
                        has_tree = True
                        break

                if 'F' in self.grid[y][x] and not has_tree:
                    #print('farmable')
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def undig(self, point):
        """Remove soil tile at given position"""
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(point):
                x = int(soil_sprite.rect.x // TILE_SIZE)
                y = int(soil_sprite.rect.y // TILE_SIZE)

                # Remove soil markers from grid
                if 'X' in self.grid[y][x]:
                    self.grid[y][x].remove('X')
                if 'W' in self.grid[y][x]:
                    self.grid[y][x].remove('W')
                if 'P' in self.grid[y][x]:
                    self.grid[y][x].remove('P')

                # Kill any plants at this position
                for plant in self.plant_sprites.sprites():
                    if plant.rect.collidepoint(point):
                        plant.kill()

                # Kill the soil tile itself
                soil_sprite.kill()

                # Recreate tiles to reflect changes
                self.create_soil_tiles()
                return True
        return False

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites:
            if soil_sprite.rect.collidepoint(target_pos):
                #print('watered')
                x = int(soil_sprite.rect.x // TILE_SIZE)
                y = int(soil_sprite.rect.y // TILE_SIZE)
                self.grid[y][x].append('W')
                pos = soil_sprite.rect.topleft
                WaterTile(pos=pos,
                          surf=pygame.image.load('images/soil/soil_water.png').convert_alpha(),
                          groups=[self.all_sprites, self.water_sprites])

    def remove_water(self):
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def check_watered(self, pos):
        x = int(pos[0] // TILE_SIZE)
        y = int(pos[1] // TILE_SIZE)
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):

                x = int(soil_sprite.rect.x // TILE_SIZE)
                y = int(soil_sprite.rect.y // TILE_SIZE)

                if 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(plant_type=seed,
                          groups=[self.all_sprites, self.plant_sprites],
                          soil=soil_sprite,
                          check_watered=self.check_watered)

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTile(pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                             surf= self.soil_surf.convert_alpha(),
                             groups=[self.all_sprites, self.soil_sprites])