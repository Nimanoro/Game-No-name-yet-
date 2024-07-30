import pygame
from healing import HealingItem

class Chest:
    def __init__(self, x, y, image_path, healing_item_image_path, healing_amount):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.scaled_image = pygame.transform.scale(self.image, (self.image.get_width() * 3, self.image.get_height() * 3))
        self.rect = self.scaled_image.get_rect(topleft=(x, y))
        self.healing_item_image_path = healing_item_image_path
        self.healing_amount = healing_amount
        self.opened = False
        self.open_images = [pygame.transform.scale(pygame.image.load(f"Animated Chests/Chests-open-{i + 1}.png").convert_alpha(), (self.image.get_width() * 3, self.image.get_height() * 3)) for i in range(2)]
        self.open_frame = 0
        self.open_duration = 1  # Time duration for each open frame
        self.last_update_time = 0  # Track the last time the frame was updated

    def open(self):
        self.opened = True
        return HealingItem(self.rect.x, self.rect.y, self.healing_item_image_path, self.healing_amount)

    def draw(self, screen):
        if self.opened:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update_time > self.open_duration * 1000:
                self.last_update_time = current_time
                self.open_frame += 1
                if self.open_frame >= len(self.open_images):
                    self.open_frame = len(self.open_images) - 1  # Stay on the last frame
            screen.blit(self.open_images[self.open_frame], self.rect)
        else:
            screen.blit(self.scaled_image, self.rect)
