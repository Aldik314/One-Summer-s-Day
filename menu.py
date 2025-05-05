import pygame
from settings import *
from timer import Timer

class Menu:
    def __init__(self, player, toggle_menu):

        #setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/Micro_5/Micro5-Regular.ttf', 50)

        #options
        self.width = 400
        self.space = 10
        self.padding = 8

        #entries

        self.options = list(self.player.item_inventory.keys())
        #print(self.options)
        self.setup()

    def setup(self):

        #create text
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + self.padding * 2

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RSHIFT]:
            self.toggle_menu()


    def show_entry(self, text_surf, amount, top):

        #background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        amount_surf = self.font.render(str(amount), False, 'black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)


    def update(self):
        self.input()
        #pygame.draw.rect(self.display_surface, 'red', self.main_rect)
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top)

            #self.display_surface.blit(text_surf, (100, text_index * 60))
        #self.display_surface.blit(pygame.Surface((1000, 1000)), (0, 0))