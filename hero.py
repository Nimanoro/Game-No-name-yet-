import pygame
import time
from key import Key

class Hero:
    def __init__(self, x, y, speed, max_hp=100, attack_damage=10):
        self.original_image = pygame.image.load('/Users/nima/Downloads/ezgif-2-dcb50d0e9a-png-100x100-sprite-png/tile000.png').convert_alpha()
        self.scaled_image = pygame.transform.scale(self.original_image, 
                            (self.original_image.get_width() * 5, self.original_image.get_height() * 5))
        self.attack_images = [
            pygame.transform.scale(pygame.image.load(f'Tiny-RPG-Character-Asset-Pack-v1.03/Characters(100x100)/Soldier/Soldier/Soldier-attack1/Soldier-Attack01-{i}.png').convert_alpha(), 
                                   (self.original_image.get_width() * 5, self.original_image.get_height() * 5))
            for i in range(5)  # Assuming 5 attack frames from 0 to 4
        ]
        self.current_image = self.scaled_image
        self.rect = self.current_image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.velocity_y = 0
        self.gravity = 0.3
        self.jump_strength = 10
        self.on_ground = False
        self.facing_right = True
        self.hp = max_hp
        self.max_hp = max_hp
        self.attack_damage = attack_damage
        self.last_damage_time = time.time()  # Initialize the last damage time
        self.attacking = False
        self.attack_cooldown = 0.5  # Attack cooldown in seconds
        self.last_attack_time = time.time()
        self.attack_frame = 0  # Track the current frame of the attack animation
        self.attack_duration = 0.5 
        self.alive = True
        self.dying = False
        self.keys = []
        self.walk_images = [pygame.transform.scale(pygame.image.load(f'Tiny-RPG-Character-Asset-Pack-v1.03/Characters(100x100)/Soldier/Soldier/Soldier-Walk/Soldier-walk copy {i + 2}.png').convert_alpha(),
                                                    (self.original_image.get_width() * 5, self.original_image.get_height() * 5))
                            for i in range(8)]
        self.walk_frame = 0
        self.walk_duration = 0.1  # Time duration for each walk frame
        self.last_walk_time = time.time()
        self.death_images = [pygame.transform.scale(pygame.image.load(f'Tiny-RPG-Character-Asset-Pack-v1.03/Characters(100x100)/Soldier/Soldier/Solider-Death/Soldier-Death-copy-{i + 1}.png').convert_alpha(),
                                                    (self.original_image.get_width() * 5, self.original_image.get_height() * 5))
                             for i in range(3)]
        self.death_frame = 0
        self.death_duration = 2  # Duration for the dying animation
        self.last_death_time = time.time()

    def move(self, keys):
        if not self.alive or self.dying:
            return

        moving = False

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.facing_right = False
            moving = True

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.facing_right = True
            moving = True

        if keys[pygame.K_UP] and self.on_ground:
            self.velocity_y = -self.jump_strength
            self.on_ground = False

        return moving

    def apply_gravity(self, platforms):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.bottom >= 880:  # Assuming the ground level is at y = 880
            self.rect.bottom = 880
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        for platform in platforms:
            if self.velocity_y >= 0 and self.rect.colliderect(platform.rect):
                if self.rect.bottom <= platform.rect.top + 10:  # Allow some threshold for landing on top
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    break

    def update(self, keys, plats):
        if self.alive:
            self.apply_gravity(plats)
            moving = self.move(keys)
            current_time = time.time()

            if self.attacking:
                if current_time - self.last_attack_time >= self.attack_duration:
                    self.attacking = False
                else:
                    self.attack_frame = int((current_time - self.last_attack_time) / self.attack_duration * len(self.attack_images))
                    if self.facing_right:
                        self.current_image = pygame.transform.flip(self.attack_images[self.attack_frame], False, False)
                    else: 
                        self.current_image = pygame.transform.flip(self.attack_images[self.attack_frame], True, False)
            elif moving:
                if current_time - self.last_walk_time >= self.walk_duration:
                    self.walk_frame = (self.walk_frame + 1) % len(self.walk_images)
                    self.last_walk_time = current_time
                if self.facing_right:
                    self.current_image = pygame.transform.flip(self.walk_images[self.walk_frame], False, False)
                else:
                    self.current_image = pygame.transform.flip(self.walk_images[self.walk_frame], True, False)
            else:
                if self.facing_right:
                    self.current_image = pygame.transform.flip(self.scaled_image, False, False)
                else:
                    self.current_image = pygame.transform.flip(self.scaled_image, True, False)

        if self.dying:
            current_time = time.time()
            if current_time - self.last_death_time >= self.death_duration / len(self.death_images):
                self.death_frame += 1
                self.last_death_time = current_time
                if self.death_frame >= len(self.death_images):
                    self.death_frame = len(self.death_images) - 1
                    self.alive = False  # End the dying animation

            self.current_image = self.death_images[self.death_frame]
            self.rect = self.current_image.get_rect(topleft=self.rect.topleft)
    
    def draw(self, screen, camera_x, camera_y):
        if not self.dying:
            self.draw_hp_bar(screen)
        
        screen.blit(self.current_image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def draw_hp_bar(self, screen):
        bar_width = 200
        bar_height = 20
        hp_percentage = self.hp / self.max_hp
        current_bar_width = bar_width * hp_percentage
        bar_x = 10
        bar_y = screen.get_height() - bar_height - 10
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, current_bar_width, bar_height))
        for key in self.keys:
            screen.blit(key.image, (bar_x, bar_y - key.image.get_height()))
        

    def check_collision(self, enemy):
        if self.rect.colliderect(enemy.rect):
            current_time = time.time()
            if current_time - self.last_damage_time >= 0.5:
                print(f"Collision detected! Hero rect: {self.rect}, Enemy rect: {enemy.rect}")
                self.take_damage(10)  # Reduce HP by 10 when colliding with the enemy
                self.last_damage_time = current_time  # Update the last damage time

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0 and not self.dying:
            self.hp = 0
            self.alive = False
            self.dying = True
            self.death_frame = 0
            self.last_death_time = time.time()
        elif self.hp > 0:
            self.alive = True

    def attack(self, enemies):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = current_time
            self.attacking = True
            self.attack_frame = 0
            if self.facing_right:
                attack_rect = pygame.Rect(self.rect.right, self.rect.top, 50, self.rect.height)
            else:
                attack_rect = pygame.Rect(self.rect.left - 50, self.rect.top, 50, self.rect.height)
            for enemy in enemies:
                if attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.attack_damage)
                    print("Enemy hit!")
    
    def heal(self, healing_amount):
        self.hp += healing_amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def interact_with_chest(self, chest):
        if not chest.opened and self.rect.colliderect(chest.rect):
            return chest.open()
        return None
    def pick_key(self, key):
        new_key = Key(key.key, key.lvl, 0, 0, key.image_path)
        self.keys.append(new_key)
    
    def remove_key(self, key):
        self.keys.remove(key)