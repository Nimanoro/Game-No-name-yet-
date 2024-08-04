import pygame
import sys
from hero import Hero
from background import Background
from enemy import Enemy
from golem import Golem
from plat import Platform
from chest import Chest


class Level1:
    def __init__(self, screen, background, game, hero):
        self.screen = screen
        self.background = background
        self.game = game
        self.clock = pygame.time.Clock()
        self.hero = hero
        self.hero.rect.topleft = (60, 60)
        self.camera_x = 0
        self.camera_y = 0

        # Load platforms and chests
        self.platforms = [
            Platform(400, 640, 100, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(200, 480, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(100, 350, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(250, 250, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(500, 150, 800, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(800, 750, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(800, 860, 400, 30, "Platforms/Cave - Platforms-copy1.png")
        ]

        self.chests = [Chest(800, 75, "Animated Chests/Chests-1.png", "Potions/healthpotiongif.gif", 60)]
        # Create hero and enemies
        self.enemies = [
            Golem(400, 50, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png"),
            Golem(700, 50, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png"),
            Golem(700, 760, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png")
        ]

        self.healing_items = []

    def run(self, keys):
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()

        self.screen.fill((255, 255, 255))  # Fill the screen with white

        # Update camera position based on the hero's position
        self.camera_x = self.hero.rect.centerx - self.screen.get_width() // 2
        self.camera_y = self.hero.rect.centery - self.screen.get_height() // 2

        # Draw background
        self.background.draw(self.screen)

        if keys[pygame.K_e]:  # Assume 'E' key is used to open the chest
            for chest in self.chests:
                if self.hero.rect.colliderect(chest.rect):
                    self.healing_items.append(chest.open())
        if keys[pygame.K_h]:
            for healing_item in self.healing_items:
                if self.hero.rect.colliderect(healing_item.rect):
                    self.hero.heal(healing_item.healing_amount)
                    self.healing_items.remove(healing_item)

        self.chests = [chest for chest in self.chests if not chest.opened]

        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        if keys[pygame.K_a]:
            self.hero.attack(self.enemies)
        for enemy in self.enemies:
            if abs(enemy.rect.x - self.hero.rect.x) < 100:
                enemy.attack(self.hero)
            enemy.update(self.platforms)

        self.hero.update(keys, self.platforms)

        # Adjust positions of game elements based on camera
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_x, self.camera_y)
        for chest in self.chests:
            chest.draw(self.screen, self.camera_x, self.camera_y)
        for healing_item in self.healing_items:
            healing_item.draw(self.screen, self.camera_x, self.camera_y)

        self.hero.draw(self.screen, self.camera_x, self.camera_y)

        # Check if hero has moved out of the screen boundaries
        if self.hero.rect.top < 0:
            self.game.transition_to_next_level()
        elif self.hero.rect.bottom > self.screen.get_height():
            self.game.transition_to_previous_level()

        pygame.display.flip()
        self.clock.tick(60)

# Make sure to call `run` once per frame in your game loop, not in an infinite loop here.
