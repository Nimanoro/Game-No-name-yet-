import pygame
class HealingItem:
    def __init__(self, x, y, image_path, healing_amount):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 2, self.image.get_height() / 2))  # Adjust the size if necessary
        self.rect = self.image.get_rect(topleft=(x, y))
        self.healing_amount = healing_amount

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))