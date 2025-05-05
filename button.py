import pygame

class Button:
    def __init__(self, x, y, image, hover_image, scale):
        self.image = pygame.transform.scale(image, (int (image.get_width() * scale), int(image.get_height() * scale)))
        self.hover_image = pygame.transform.scale(hover_image, (int(hover_image.get_width() * scale), int(hover_image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_hovered = False

    def draw(self, surface):
        pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(pos)
        surface.blit(
            self.hover_image if self.is_hovered else self.image,
            (self.rect.x, self.rect.y)
        )

    def click_check(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            return self.is_hovered  # Only return True if clicked while hovering
        return False