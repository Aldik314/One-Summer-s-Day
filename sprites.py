import pygame
from settings import *
from timer import Timer
from random import randint, choice

from abc import ABC, abstractmethod
class Damageable(ABC):
    @abstractmethod
    def damage(self): pass

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

    @abstractmethod
    def update(self, dt): pass

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name

class Water(Generic):
    def __init__(self, pos, frames, groups, z):

        #animation
        self.frames = frames
        self.frame_index = 0

        #sprite
        super().__init__(pos = pos, surf = self.frames[self.frame_index], groups = groups, z = LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 1*dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class Flower(Generic):
    def __init__(self, pos, surf, groups, main_render_group, player_add):
        super().__init__(pos, surf, groups)
        self.main_render_group = main_render_group


class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        #white surf
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic, Damageable):
    def __init__(self, pos, surf, groups, main_render_group, player_add):
        super().__init__(pos, surf, groups)
        self.main_render_group = main_render_group
        self.player_add = player_add
        self.invul_timer = Timer(200)
        self.apple_surf = pygame.image.load('images/objects/apple.png')
        self.apple_position = apple_pos
        self.apple_sprites = pygame.sprite.Group()
        self.occupied_positions = set()

        # New: Track days until next regrowth
        self.days_until_regrowth = 0
        self.initialize_apples()

    def initialize_apples(self):
        """Create initial apples (minimum 1 per tree)"""
        available_positions = list(range(len(self.apple_position)))

        # Always spawn at least 1 apple
        if not self.occupied_positions:
            pos_idx = choice(available_positions)
            self.spawn_apple(pos_idx)
            available_positions.remove(pos_idx)

        # 50% chance for additional apples
        for pos_idx in available_positions:
            if randint(0, 1) == 0:
                self.spawn_apple(pos_idx)

        # Schedule first regrowth in 1-3 days
        self.schedule_next_regrowth()

    def schedule_next_regrowth(self):
        """Set timer for next regrowth (1-3 days)"""
        self.days_until_regrowth = randint(1, 3)

    def spawn_apple(self, pos_idx):
        """Create an apple at specific position"""
        pos = self.apple_position[pos_idx]
        x = pos[0] + self.rect.left
        y = pos[1] + self.rect.top

        Generic(
            pos=(x, y),
            surf=self.apple_surf.convert_alpha(),
            groups=[self.apple_sprites, self.main_render_group],
            z=LAYERS['fruit']
        )
        self.occupied_positions.add(pos_idx)

    def damage(self):
        """When tree is damaged/harvested"""
        if self.apple_sprites:
            apple = choice(list(self.apple_sprites))
            pos_idx = next(
                i for i, pos in enumerate(self.apple_position)
                if (pos[0] + self.rect.left, pos[1] + self.rect.top) == apple.rect.topleft
            )

            self.occupied_positions.remove(pos_idx)
            self.create_harvest_particles(apple)
            self.player_add('apple')
            apple.kill()

    def create_harvest_particles(self, apple):
        Particle(
            pos=apple.rect.topleft,
            surf=apple.image,
            groups=[self.main_render_group],
            z=LAYERS['fruit']
        )

    def new_day(self):
        """Call this when a new day starts in your game"""
        if self.days_until_regrowth > 0:
            self.days_until_regrowth -= 1

        if self.days_until_regrowth == 0 and self.occupied_positions != set(range(len(self.apple_position))):
            self.regrow_apple()
            self.schedule_next_regrowth()

    def regrow_apple(self):
        """Regrow one missing apple"""
        missing_positions = [
            i for i in range(len(self.apple_position))
            if i not in self.occupied_positions
        ]
        if missing_positions:
            self.spawn_apple(choice(missing_positions))

    def update(self, dt):
        """Handle any time-based updates"""
        if self.invul_timer.active:
            self.invul_timer.update()

class Block(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy()