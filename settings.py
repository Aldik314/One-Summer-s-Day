from pygame.math import Vector2
#scale
import pygame
sc = 0.6
tsc = 80*sc

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 750
TILE_SIZE = tsc

#overlay settings
OVERLAY_POSITIONS = {
    'tool': (50, SCREEN_HEIGHT + 10),
    'seed': (130, SCREEN_HEIGHT + 10)
}

player_tool_offset = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -5),
    'down': Vector2(0, 75)
}

LAYERS = {
    'water': 0,
    'ground': 1,
    'shadow': 2,
    'soil': 3,
    'soil water': 4,
    'rain floor': 5,
    'house bottom': 6,
    'ground plant': 7,
    'main': 8,
    'house top': 9,
    'fruit': 10,
    'rain drops': 11
}

farmable_pos = {
    (17, 4),
    (17, 5),
    (17, 6),
    (17, 7),
    (17, 8),
    (17, 9),
    (18, 3),
    (18, 4),
    (18, 5),
    (18, 6),
    (18, 7),
    (18, 8),
    (18, 9),
    (18, 10),
    (19, 2),
    (19, 3),
    (19, 4),
    (19, 5),
    (19, 6),
    (19, 7),
    (19, 8),
    (19, 9),
    (19, 10),
    (19, 11),
    (20, 2),
    (20, 3),
    (20, 4),
    (20, 5),
    (20, 6),
    (20, 7),
    (20, 8),
    (20, 9),
    (20, 10),
    (20, 11),
    (21, 2),
    (21, 3),
    (21, 4),
    (21, 5),
    (21, 6),
    (21, 7),
    (21, 8),
    (21, 9),
    (21, 10),
    (21, 11),
    (22, 2),
    (22, 3),
    (22, 4),
    (22, 5),
    (22, 6),
    (22, 7),
    (22, 8),
    (22, 9),
    (22, 10),
    (22, 11),
    (23, 3),
    (23, 4),
    (23, 5),
    (23, 6),
    (23, 7),
    (23, 8),
    (23, 9),
    (23, 10),
    (23, 11),
    (24, 3),
    (24, 4),
    (24, 5),
    (24, 6),
    (24, 7),
    (24, 8),
    (24, 9),
    (24, 10),
    (24, 11),
    (25, 4),
    (25, 5),
    (25, 6),
    (25, 7),
    (25, 8),
    (25, 9),
    (25, 10)
}

flower_positions = [
    (3, 4),
    (5, 1),
    (12, 0),
    (15, 3),
    (14, 11),
    (17, 0),
    (25, 0)
]

tree_pos = [
    (17, 2),
    (22, 1)
]

collision_pos = [
    (1,0),
    (1,1),
    (1,2),
    (1,3),
    (1,4),
    (1,5),
    (1,6),
    (1,7),
    (1,8),
    (1,9),
    (1,10),
    (1,11),
    (1,12),
    (1,13),
    (2,13),
    (3,13),
    (4,13),
    (5,13),
    (6,13),
    (7,13),
    (8,13),
    (9,13),
    (10,13),
    (11,13),
    (12,13),
    (13,13),
    (14,13),
    (15,13),
    (16,13),
    (17,13),
    (18,13),
    (19,13),
    (20,13),
    (21,13),
    (22,13),
    (23,13),
    (24,13),
    (25,13),
    (26, 13),
    (7, 6),
    (8, 6),
    (9, 6),
    (10, 6),
    (11, 6),
    (7, 5),
    (8, 5),
    (9, 5),
    (10, 5),
    (11, 5),
    (7, 4),
    (8, 4),
    (9, 4),
    (10, 4),
    (11, 4)
]

border1 = [
    (2, 0),
    (3, 0),
    (4, 0),
    (5, 0),
    (6, 0),
    (7, 0),
    (8, 0),
    (9, 0),
    (10, 0),
    (11, 0),
    (12, 0),
    (13, 0),
    (14, 0),
    (15, 0),
    (16, 0),
    (17, 0),
    (18, 0),
    (19, 0),
    (20, 0),
    (21, 0),
    (22, 0),
    (23, 0),
    (24, 0),
    (25, 0),
    (26, 0)
]

border2 = [
    (26, 0),
    (26, 1),
    (26, 2),
    (26, 3),
    (26, 4),
    (26, 5),
    (26, 6),
    (26, 7),
    (26, 8),
    (26, 9),
    (26, 10),
    (26, 11),
    (26, 12),
    (26, 13)
]

apple_pos = [(43, 46), (78, 2), (68, 26), (77, 54), (34, 15)]

house_surf = pygame.image.load('images/layers/house.png')
h_width = int(house_surf.get_width() * sc)
h_height = int(house_surf.get_height() * sc)
house_surf = pygame.transform.scale(house_surf, (h_width, h_height))

s_post_surf = pygame.image.load('images/layers/s_post.png')
sp_width = int(s_post_surf.get_width() * sc)
sp_height = int(s_post_surf.get_height() * sc)
s_post_surf = pygame.transform.scale(s_post_surf, (sp_width, sp_height))

post_surf = pygame.image.load('images/layers/post.png')
p_width = int(post_surf.get_width() * sc)
p_height = int(post_surf.get_height() * sc)
post_surf = pygame.transform.scale(post_surf, (p_width, p_height))

s_fence_surf = pygame.image.load('images/layers/s_fence.png')
sfe_width = int(s_fence_surf.get_width() * sc)
sfe_height = int(s_fence_surf.get_height() * sc)
s_fence_surf = pygame.transform.scale(s_fence_surf, (sfe_width, sfe_height))

fence1_surf = pygame.image.load('images/layers/fence_1.png')
fe1_width = int(fence1_surf.get_width() * sc)
fe1_height = int(fence1_surf.get_height() * sc)
fence1_surf = pygame.transform.scale(fence1_surf, (fe1_width, fe1_height))

fence2_surf = pygame.image.load('images/layers/fence_2.png')
fe2_width = int(fence2_surf.get_width() * sc)
fe2_height = int(fence2_surf.get_height() * sc)
fence2_surf = pygame.transform.scale(fence2_surf, (fe2_width, fe2_height))

path_surf = pygame.image.load('images/layers/path.png')
pa_width = int(path_surf.get_width() * sc)
pa_height = int(path_surf.get_height() * sc)
path_surf = pygame.transform.scale(path_surf, (pa_width, pa_height))

s_bridge_surf = pygame.image.load('images/layers/s_bridge.png')
sb_width = int(s_bridge_surf.get_width() * sc)
sb_height = int(s_bridge_surf.get_height() * sc)
s_bridge_surf = pygame.transform.scale(s_bridge_surf, (sb_width, sb_height))

bridge_surf2 = pygame.image.load('images/layers/bridge_2.png')
b2_width = int(bridge_surf2.get_width() * sc)
b2_height = int(bridge_surf2.get_height() * sc)
bridge_surf2 = pygame.transform.scale(bridge_surf2, (b2_width, b2_height))

bridge_surf1 = pygame.image.load('images/layers/bridge_1.png')
b1_width = int(bridge_surf1.get_width() * sc)
b1_height = int(bridge_surf1.get_height() * sc)
bridge_surf1 = pygame.transform.scale(bridge_surf1, (b1_width, b1_height))

bridge_surf3 = pygame.image.load('images/layers/bridge_3.png')
b3_width = int(bridge_surf3.get_width() * sc)
b3_height = int(bridge_surf3.get_height() * sc)
bridge_surf3 = pygame.transform.scale(bridge_surf3, (b3_width, b3_height))

flower_surf = pygame.image.load('images/objects/flower.png')

tree_surf = pygame.image.load('images/objects/tree.png')