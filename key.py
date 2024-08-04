import pygame

class Key:
    def __init__(self, key, lvl, x, y, image_path):
        self.key = key
        self.lvl = lvl
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_path = image_path

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))