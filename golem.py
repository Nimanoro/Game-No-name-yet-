import pygame
import time
import sys

class Golem:
    def __init__(self, x, y, speed, image_path, max_hp=100):
        try:
            self.original_image = pygame.image.load(image_path).convert_alpha()
            print(f"Loaded enemy image from {image_path}")
            self.scaled_image = pygame.transform.scale(
                self.original_image,
                (self.original_image.get_width() * 3, self.original_image.get_height() * 3)
            )
            self.y = y
            self.current_image = pygame.transform.flip(self.scaled_image, True, False)
            self.rect = self.current_image.get_rect()
            self.rect.topleft = (x, y)
            self.speed = speed
            self.facing_right = True
            self.hp = max_hp
            self.max_hp = max_hp
            self.alive = True
            self.last_attack_time = time.time()
            self.attack_damage = 40
            self.last_damage_time = time.time()
            self.attacking = False
            self.walking = False
            self.attack_cooldown = 1
            self.last_attack_time = time.time()
            self.attack_frame = 0
            self.attack_duration = 1
            self.alive = True

            # Load walking images
            self.walk_images = [pygame.transform.scale(pygame.image.load(f'Golem_1/Blue/No_Swoosh_VFX/walk/Golem_1_walk copy-{i + 1}.png').convert_alpha(),
                                                       (self.original_image.get_width() * 3, self.original_image.get_height() * 3))
                                for i in range(9)]
            self.walk_frame = 0
            self.walk_duration = 0.1  # Time duration for each walk frame
            self.last_walk_time = time.time()

            # Load attack images
            self.attack_images = [pygame.transform.scale(pygame.image.load(f'Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-{i + 1}.png').convert_alpha(),
                                                         (self.original_image.get_width() * 3, self.original_image.get_height() * 3))
                                  for i in range(9)]
        except pygame.error as e:
            print(f"Error loading image: {e}")
            sys.exit(1)

    def move(self, platforms):
        if not self.alive:
            return

        screen_width = pygame.display.get_surface().get_width()

        # Update walk frame based on time
        current_time = time.time()
        if current_time - self.last_walk_time >= self.walk_duration:
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_images)
            self.last_walk_time = current_time

        # Assume the Golem is not on any platform initially
        on_platform = False

       

        # Move the enemy horizontally

        # Check if the Golem is on a platform and handle edge detection
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and abs(self.rect.bottom - platform.rect.top) < 20:
                on_platform = True
                if self.facing_right and self.rect.right >= platform.rect.right:
                    self.rect.right = platform.rect.right
                    self.speed = -self.speed
                    self.facing_right = not self.facing_right
                elif not self.facing_right and self.rect.left <= platform.rect.left:
                    self.rect.left = platform.rect.left
                    self.speed = -self.speed
                    self.facing_right = not self.facing_right


        # If the Golem reaches the edge of the screen, reverse direction
        if self.rect.left <= 0 or self.rect.right >= screen_width:
            self.speed = -self.speed
            self.facing_right = not self.facing_right
        if self.rect.bottom >= 800:
            on_platform = True
        if not on_platform:
            self.speed = -self.speed

        # Set current image to the current walk fram
        self.rect.x += self.speed


        if self.facing_right:
            self.current_image = pygame.transform.flip(self.walk_images[self.walk_frame], False, False)
        else:
            self.current_image = pygame.transform.flip(self.walk_images[self.walk_frame], True, False)

    def update(self, platforms):
        self.move(platforms)
        if self.attacking:
            current_time = time.time()
            if current_time - self.last_attack_time >= self.attack_duration:
                self.attacking = False
            else:
                self.attack_frame = int((current_time - self.last_attack_time) / self.attack_duration * len(self.attack_images))
                if self.facing_right:
                    self.current_image = pygame.transform.flip(self.attack_images[self.attack_frame], False, False)
                else:
                    self.current_image = pygame.transform.flip(self.attack_images[self.attack_frame], True, False)
        else:
            if self.facing_right:
                self.current_image = pygame.transform.flip(self.walk_images[self.walk_frame], False, False)
            else:
                self.current_image = pygame.transform.flip(self.walk_images[self.walk_frame], True, False)

        self.rect = self.current_image.get_rect(topleft=self.rect.topleft)

    def draw(self, screen):
        self.draw_hp_bar(screen)
        screen.blit(self.current_image, self.rect)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def draw_hp_bar(self, screen):
        bar_width = 100
        bar_height = 10
        hp_percentage = self.hp / self.max_hp
        current_bar_width = bar_width * hp_percentage
        bar_x = self.rect.x + (self.rect.width - bar_width) / 2
        bar_y = self.rect.y - bar_height - 5
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, current_bar_width, bar_height))

    def attack(self, hero):
        current_time = time.time()
        if -50 < self.rect.y - hero.rect.y < 50 and ((self.facing_right and hero.rect.x > self.rect.x ) or (hero.rect.x < self.rect.x and not self.facing_right)) and current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.attacking = True
            self.attack_frame = 0
            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right, self.rect.top, 50, self.rect.height)
            else:
                attack_rect = pygame.Rect(self.rect.left - 50, self.rect.top, 50, self.rect.height)
            if attack_rect.colliderect(hero.rect):
                hero.take_damage(self.attack_damage)
