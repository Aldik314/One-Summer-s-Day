import pygame
from settings import *

class Overlay:
    def __init__(self, player):

        #gen setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        #imports
        overlay_path = 'images/overlay/'
        self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in player.tools}
        self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}

    def display(self):
        # tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        new_width = int(tool_surf.get_width() * 0.8)
        new_height = int(tool_surf.get_height() * 0.8)
        tool_surf = pygame.transform.scale(tool_surf, (new_width, new_height))
        self.display_surface.blit(tool_surf, tool_rect)

        #seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        new_width = int(seed_surf.get_width() * 0.8)
        new_height = int(seed_surf.get_height() * 0.8)
        seed_surf = pygame.transform.scale(seed_surf, (new_width, new_height))
        self.display_surface.blit(seed_surf, seed_rect)