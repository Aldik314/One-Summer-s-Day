import pygame
from settings import *
from support import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, menu_page):
        super().__init__(group)

        self.import_assets()
        self.status = 'down'
        self.frame_index = 0

        #general
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['main']

        #movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        #collision
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.8, -self.rect.width * 0.7)

        #timers
        self.timers = {
            'tool use': Timer(600, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(600, self.use_seed),
            'seed switch': Timer(200)
        }

        #tools
        self.tools = ['hoe', 'axe', 'water', 'pickaxe']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        #seeds
        self.seeds = ['carrot', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        #inventory
        self.item_inventory = {
            'apple':  0,
            'carrot': 0,
            'tomato': 0
        }

        #interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.sleep = False
        self.soil_layer = soil_layer
        self.menu_page = menu_page

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        if self.selected_tool == 'pickaxe':
            pass
        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
        if self.selected_tool == 'axe':
            self.soil_layer.undig(self.target_pos)
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()

    def get_target_pos(self):
        self.target_pos = self.rect.center + player_tool_offset[self.status.split('_')[0]]

    def use_seed(self):
        self.soil_layer.plant_seed(self.target_pos, self.selected_seed)

    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
                           'up_axe': [], 'down_axe': [], 'left_axe': [], 'right_axe': [],
                           'up_pickaxe': [], 'down_pickaxe': [], 'left_pickaxe': [], 'right_pickaxe': [],
                           'up_hoe': [], 'down_hoe': [], 'left_hoe': [], 'right_hoe': [],
                           'up_water': [], 'down_water': [], 'left_water': [], 'right_water': []}

        for animation in self.animations.keys():
            full_path = 'images/movement/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
            #directions
            if keys[pygame.K_w] and self.direction.y < 100:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            #tool use
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            #change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]

            #seed use
            if keys[pygame.K_t]:
                self.timers['seed use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                #print('use seed')

            #change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                self.seed_index = self.seed_index if self.seed_index < len(self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]
                #print(self.selected_seed)

            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Enter':
                        self.status = 'up_idle'
                        self.sleep = True

            if keys[pygame.K_LSHIFT]:
                self.menu_page()

    def get_status(self):

        #idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        #tool
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Calculate proposed movement
        new_pos = pygame.math.Vector2(self.pos)
        new_pos += self.direction * self.speed * dt

        # Create a proposed hitbox
        new_hitbox = self.hitbox.copy()
        new_hitbox.centerx = round(new_pos.x)
        new_hitbox.centery = round(new_pos.y)

        # Check for collisions with proposed position
        collision = False
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox') and new_hitbox.colliderect(sprite.hitbox):
                collision = True
                break

        # Only update position if no collision
        if not collision:
            self.pos = new_pos
            self.hitbox.center = round(self.pos.x), round(self.pos.y)
            self.rect.center = self.hitbox.center
        else:
            # Try horizontal movement only
            temp_hitbox = self.hitbox.copy()
            temp_hitbox.centerx = round(new_pos.x)

            h_collision = False
            for sprite in self.collision_sprites:
                if hasattr(sprite, 'hitbox') and temp_hitbox.colliderect(sprite.hitbox):
                    h_collision = True
                    break

            if not h_collision:
                self.pos.x = new_pos.x
                self.hitbox.centerx = round(self.pos.x)
                self.rect.centerx = self.hitbox.centerx

            # Try vertical movement only
            temp_hitbox = self.hitbox.copy()
            temp_hitbox.centery = round(new_pos.y)

            v_collision = False
            for sprite in self.collision_sprites:
                if hasattr(sprite, 'hitbox') and temp_hitbox.colliderect(sprite.hitbox):
                    v_collision = True
                    break

            if not v_collision:
                self.pos.y = new_pos.y
                self.hitbox.centery = round(self.pos.y)
                self.rect.centery = self.hitbox.centery

    def check_collision(self, direction):
        """Basic blocking collision with all objects"""
        for sprite in self.collision_sprites:
            if hasattr(sprite, 'hitbox') and sprite.hitbox.colliderect(self.hitbox):
                self.resolve_collision(sprite, direction)
                break  # Only resolve one collision per axis

    def resolve_collision(self, sprite, direction):
        """Simple collision resolution - stops movement"""
        if direction == 'horizontal':
            if self.direction.x > 0:  # Moving right
                self.hitbox.right = sprite.hitbox.left
            elif self.direction.x < 0:  # Moving left
                self.hitbox.left = sprite.hitbox.right
            self.pos.x = self.hitbox.centerx

        elif direction == 'vertical':
            if self.direction.y > 0:  # Moving down
                self.hitbox.bottom = sprite.hitbox.top
            elif self.direction.y < 0:  # Moving up
                self.hitbox.top = sprite.hitbox.bottom
            self.pos.y = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)