import pygame

class Platform:
    def __init__(self, x, y, w, h, image_path):
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (w, h))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.top = y + self.image.get_height()
        
        self.width = (x, x + self.image.get_width())

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
