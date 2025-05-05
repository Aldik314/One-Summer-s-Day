import pygame
from settings import *
from player import Player
from overlay import Overlay
from sprites import *
from support import *
from transition import Transition
from soil import *
from menu import Menu
import json

class Level:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:  # Prevent re-initialization
            return

        #get the display surface
        self.display_surface = pygame.display.get_surface()

        #sprites
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.flower_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()
        self.soil_layer = SoilLayer(
            all_sprites=self.all_sprites,
            tree_sprites=self.tree_sprites
        )

        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        #menu
        self.menu = Menu(self.player, self.menu_page)
        self.menu_active = False

    def setup(self, destroyed_trees=None, destroyed_flowers=None):

        #house
        Generic(pos = (7 * TILE_SIZE - 12, 7 * TILE_SIZE - 270),
                surf = house_surf.convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['main'])

        #postbox
        Generic(pos = (12 * TILE_SIZE, 6 * TILE_SIZE + 15),
                surf = s_post_surf.convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['shadow'])

        Generic(pos=(12 * TILE_SIZE, 6 * TILE_SIZE + 15),
                surf=post_surf.convert_alpha(),
                groups=[self.all_sprites, self.collision_sprites],
                z=LAYERS['main'])

        #fence
        Generic(pos=(6 * TILE_SIZE + 9, 6 * TILE_SIZE - 24),
                surf=s_fence_surf.convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['shadow'])

        Generic(pos=(6 * TILE_SIZE + 12, 6 * TILE_SIZE - 24),
                surf=fence1_surf.convert_alpha(),
                groups=[self.all_sprites, self.collision_sprites],
                z=LAYERS['main'])

        Generic(pos=(7 * TILE_SIZE - 12, 9 * TILE_SIZE - 33),
                surf=fence2_surf.convert_alpha(),
                groups=[self.all_sprites, self.collision_sprites],
                z=LAYERS['main'])

        #path
        Generic(pos = (10 * TILE_SIZE - 9, 8 * TILE_SIZE),
                surf = path_surf.convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['soil'])

        #bridge
        Generic(pos = (0 * TILE_SIZE, 5 * TILE_SIZE + 18),
                surf = s_bridge_surf.convert_alpha(),
                groups = self.all_sprites,
                z = LAYERS['shadow'])

        Generic(pos=(0 * TILE_SIZE, 2 * TILE_SIZE - 9),
                surf=bridge_surf3.convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['main'])

        Generic(pos=(0 * TILE_SIZE, 3 * TILE_SIZE),
                surf=bridge_surf1.convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['soil'])

        Generic(pos=(0 * TILE_SIZE, 4 * TILE_SIZE + 6),
                surf=bridge_surf2.convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['main'])

        #collision tiles
        for x_tile, y_tile in collision_pos:
            Block(pos=(x_tile * TILE_SIZE, y_tile * TILE_SIZE),
                surf=pygame.Surface((TILE_SIZE, TILE_SIZE)),
                groups = self.collision_sprites)

        Block(
            pos=(12 * TILE_SIZE + 12, 7 * TILE_SIZE - 18),
            surf=pygame.Surface((36, 18)),
            groups = self.collision_sprites
        )

        Block(
            pos=(6 * TILE_SIZE + 3, 9 * TILE_SIZE - 30),
            surf=pygame.Surface((138, 21)),
            groups = self.collision_sprites
        )

        Block(
            pos=(6 * TILE_SIZE + 3, 6 * TILE_SIZE - 33),
            surf=pygame.Surface((38, 144)),
            groups = self.collision_sprites
        )

        for x_tile, y_tile in border1:
            Block(pos=(x_tile * TILE_SIZE, y_tile * TILE_SIZE),
                surf=pygame.Surface((TILE_SIZE, 30)),
                groups = self.collision_sprites)

        for x_tile, y_tile in border2:
            Block(pos=(x_tile * TILE_SIZE + 21, y_tile * TILE_SIZE),
                surf=pygame.Surface((TILE_SIZE, TILE_SIZE)),
                groups = self.collision_sprites)

        # player
        self.player = Player(pos = (429, 291),
                             group = self.all_sprites,
                             collision_sprites=self.collision_sprites,
                             tree_sprites = self.tree_sprites,
                             interaction = self.interaction_sprites,
                             soil_layer = self.soil_layer,
                             menu_page=self.menu_page
                             )
        Interaction(pos= (10 * TILE_SIZE, 8 * TILE_SIZE),
                    size= (TILE_SIZE, TILE_SIZE),
                    groups= self.interaction_sprites,
                    name= 'Enter')

        # world
        Generic(pos=(0, 0),
                surf=pygame.image.load('images/layers/world.png').convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['ground'])

        #water
        water_frames = import_folder_without_sc('images/layers/water')
        Water(pos = (0, 0),
              frames = water_frames,
              groups = self.all_sprites,
              z = LAYERS['water'])

        #flowers
        for x_tile, y_tile in flower_positions:
            Flower(
                pos=(x_tile * TILE_SIZE, y_tile * TILE_SIZE),
                surf=flower_surf.convert_alpha(),
                groups=[self.all_sprites, self.collision_sprites, self.flower_sprites],
                main_render_group=self.all_sprites,
                player_add=self.player_add
            )

            # trees - only create if not destroyed
        for x_tile, y_tile in tree_pos:
            Tree(
                pos=(x_tile * TILE_SIZE, y_tile * TILE_SIZE),
                surf=tree_surf.convert_alpha(),
                groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                main_render_group=self.all_sprites,
                player_add=self.player_add
            )

    def save_game(self, save_file = 'save.json'):
        save_data = {
            'player': {
                'pos': (self.player.rect.x, self.player.rect.y),
                'inventory': self.player.item_inventory,
                'selected_tool': self.player.selected_tool,
                'selected_seed': self.player.selected_seed
            },
            'soil_grid': self.soil_layer.grid,
            'plants': [
                {
                    'pos': (plant.rect.x, plant.rect.y),
                    'type': plant.plant_type,
                    'age': plant.age
                }
                for plant in self.soil_layer.plant_sprites
            ]
        }
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=4)

    def load_game(self, save_file='save.json'):
        try:
            with open(save_file, 'r') as f:
                save_data = json.load(f)

            # Load player data
            self.player.rect.topleft = save_data['player']['pos']
            self.player.item_inventory = save_data['player']['inventory']
            self.player.selected_tool = save_data['player']['selected_tool']
            self.player.selected_seed = save_data['player']['selected_seed']

            # Reset world first
            self.soil_layer.grid = save_data['soil_grid']
            self.soil_layer.create_soil_tiles()

            # Recreate plants
            self.soil_layer.plant_sprites.empty()
            for plant_data in save_data['plants']:
                soil_sprite = self.find_soil_at_pos(plant_data['pos'])
                if soil_sprite:
                    plant = Plant(
                        plant_type=plant_data['type'],
                        groups=[self.all_sprites, self.soil_layer.plant_sprites],
                        soil=soil_sprite,
                        check_watered=self.soil_layer.check_watered
                    )
                    plant.age = plant_data['age']

            return True
        except (FileNotFoundError, json.JSONDecodeError):
            return False  # No save file found

    def find_soil_at_pos(self, pos):
        for sprite in self.soil_layer.soil_sprites:
            if sprite.rect.collidepoint(pos):
                return sprite
        return None

    def player_add(self, item):

        self.player.item_inventory[item] += 1
        #print(self.player.item_inventory)

    def menu_page(self):
        self.menu_active = not self.menu_active
        #print(f"Menu Active: {self.menu_active}")

    def reset(self):
        self.save_game()
        # apples
        for tree in self.tree_sprites:
            tree.new_day()

        self.soil_layer.update_plants()
        self.soil_layer.remove_water()

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(pos=plant.rect.topleft,
                             surf=plant.image,
                             groups=self.all_sprites,
                             z=LAYERS['main'])
                    self.soil_layer.grid[int(plant.rect.centery // TILE_SIZE)][int(plant.rect.centerx // TILE_SIZE)].remove('P')

    def run(self, dt):

        #drawing logic
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)

        if self.menu_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()

        self.overlay.display()

        if self.player.sleep:
            self.transition.play()

        #print(self.menu_active)
        #print(self.player.item_inventory)

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx# - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery# - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.bottom):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    #offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    #to check
                    #if sprite == player:
                        #pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                        #hitbox_rect = player.hitbox.copy()
                        #hitbox_rect.center = offset_rect.center
                        #pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
                        #target_pos = offset_rect.center + player_tool_offset[player.status.split('_')[0]]
                        #pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)