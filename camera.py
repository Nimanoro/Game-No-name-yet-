import pygame
import sys

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to the size of the level
        x = min(0, x)  # Left boundary
        y = min(0, y)  # Top boundary
        self.camera = pygame.Rect(x, y, self.width, self.height)
