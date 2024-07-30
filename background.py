import pygame

class Background:
    def __init__(self, image_path, screen_width, screen_height):
        self.image = pygame.image.load(image_path).convert()
        self.image = pygame.transform.scale(self.image, (screen_width, screen_height))
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
