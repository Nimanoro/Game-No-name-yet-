import pygame
import sys

class Enemy:
    def __init__(self, x, y, speed, image_path, max_hp=100):
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            print(f"Loaded enemy image from {image_path}")
            self.scaled_image = pygame.transform.scale(
                self.original_image,
                (self.original_image.get_width() * 5, self.original_image.get_height() * 5)
            )
            self.current_image = pygame.transform.flip(self.scaled_image, True, False)
            self.rect = self.current_image.get_rect()
            self.rect.topleft = (x, y)
            self.speed = speed
            self.facing_right = True
            self.hp = max_hp
            self.max_hp = max_hp
            self.alive = True
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit(1)
            
    def move(self):
        if not self.alive:
            return
         
        screen_width = pygame.display.get_surface().get_width()
        
        # Move the enemy
        self.rect.x += self.speed
        
        # Check for boundary collision and reverse direction if necessary
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed = -self.speed
            self.facing_right = not self.facing_right
        
        # Flip the image if the direction changes
        if self.facing_right:
            self.current_image = self.scaled_image
        else:
            self.current_image = pygame.transform.flip(self.scaled_image, True, False)
        

    def draw(self, screen):
        self.draw_hp_bar(screen)
        screen.blit(self.current_image, self.rect)


    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0  # Ensure HP doesn't go below 0
            self.alive = False

    
    def draw_hp_bar(self, screen):
        # Define the width and height of the health bar
        bar_width = 100
        bar_height = 10
        hp_percentage = self.hp / self.max_hp
        current_bar_width = bar_width * hp_percentage
        bar_x = self.rect.x + (self.rect.width - bar_width) / 2
        bar_y = self.rect.y - bar_height - 5 
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, current_bar_width, bar_height))

    
