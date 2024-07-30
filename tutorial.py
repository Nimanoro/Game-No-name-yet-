import pygame
import sys
from hero import Hero
from background import Background
from enemy import Enemy
from golem import Golem
from plat import Platform
from chest import Chest

class Tutorial:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set the display mode to full screen and resizable
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
        pygame.display.set_caption("Sword Game")

        # Load background
        self.background = Background("Free-Pixel-Art-Forest/Preview/Background.png", self.screen.get_width(), self.screen.get_height())

        # Load key images
        self.arrow_left_image = pygame.image.load("Individual Icons/keyboard_73.png")
        self.arrow_right_image = pygame.image.load("Individual Icons/keyboard_72.png")
        self.e_key_image = pygame.image.load("Individual Icons/keyboard_15.png")
        self.h_key_image = pygame.image.load("Individual Icons/keyboard_28.png")
        self.a_key_image = pygame.image.load("Individual Icons/keyboard_23.png")
        self.arrow_up_image = pygame.image.load("Individual Icons/keyboard_70.png")

        # Transform the images to fit the screen appropriately
        key_width, key_height = 50, 50
        self.arrow_left_image = pygame.transform.scale(self.arrow_left_image, (key_width, key_height))
        self.arrow_right_image = pygame.transform.scale(self.arrow_right_image, (key_width, key_height))
        self.arrow_up_image = pygame.transform.scale(self.arrow_up_image, (key_width, key_height))
        self.a_key_image = pygame.transform.scale(self.a_key_image, (key_width, key_height))
        self.e_key_image = pygame.transform.scale(self.e_key_image, (key_width, key_height))
        self.h_keu_image = pygame.transform.scale(self.h_key_image, (key_width, key_height))

        # Initial positions (center of the screen)
        self.left_key_initial_pos = (self.screen.get_width() // 2 - key_width - 10, self.screen.get_height() // 2)
        self.right_key_initial_pos = (self.screen.get_width() // 2 + 10, self.screen.get_height() // 2)
        self.up_key_inital_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 - key_height - 10)

        self.a_key_initial_pos = (self.screen.get_width() // 2 + 2 * key_width , self.screen.get_height() // 2)
        self.e_key_initial_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 + key_height + 20 + 10)
        self.h_key_initial_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 + key_height + 20 + 10)
        
        # Flags to control the display of key images
        self.show_left_arrow = True
        self.show_right_arrow = True
        self.show_a_key = True
        self.show_up_arrow = True
        self.show_e_key = False
        self.show_h_key = False


        # Flags to check if keys have been pressed
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.up_key_pressed = False
        self.space_key_pressed = False
        self.chest_encountered = False

        # Flags to control tutorial state
        self.tutorial_running = True

        self.platforms = [
            Platform(800, 750, 50, 30, "Platforms/Cave - Platforms-copy1.png")
        ]

        self.chests = [Chest(800, 810, "Animated Chests/Chests-1.png", "Potions/healthpotiongif.gif", 40)]
        # Create hero
        self.hero = Hero(200, 820, 5)

        self.healing_items = []
        self.enemies = [Golem(600, 760, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png", 20)]

        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.screen.fill((255, 255, 255))  # Fill the screen with white
            self.background.draw(self.screen)

            if self.tutorial_running:
                # Show the key hints in the center of the screen
                if not self.left_key_pressed:
                    self.screen.blit(self.arrow_left_image, self.left_key_initial_pos)
                if not self.right_key_pressed:
                    self.screen.blit(self.arrow_right_image, self.right_key_initial_pos)
                if not self.space_key_pressed:
                    self.screen.blit(self.a_key_image, self.a_key_initial_pos)
                if not self.up_key_pressed:
                    self.screen.blit(self.arrow_up_image, self.up_key_inital_pos)
                # Check for key presses to complete the tutorial
                if keys[pygame.K_LEFT]:
                    self.left_key_pressed = True
                    self.show_left_arrow = False
                if keys[pygame.K_RIGHT]:
                    self.right_key_pressed = True
                    self.show_right_arrow = False
                if keys[pygame.K_UP]:
                    self.up_key_pressed = True
                    self.show_up_arrow = False
                if keys[pygame.K_a]:
                    self.space_key_pressed = True
                    self.show_a_key = False
                if keys[pygame.K_e] and self.show_e_key:
                    self.show_e_key = False

                # Resume the game if all tutorial keys have been pressed
                if self.left_key_pressed and self.right_key_pressed and self.space_key_pressed:
                    self.tutorial_running = False
            else:
                # Update and draw game elements
                if self.hero.rect.colliderect(self.chests[0].rect) and not self.chest_encountered:
                    self.show_e_key = True
                    self.chest_encountered = True
                if self.show_e_key:
                    self.screen.blit(self.e_key_image, self.e_key_initial_pos) 

                for healing_item in self.healing_items:
                    if self.hero.rect.colliderect(healing_item.rect):
                        self.show_h_key = True
                        self.healing_item_encountered = True

                if self.show_h_key:
                    self.screen.blit(self.h_key_image, self.h_key_initial_pos)
            
                if keys[pygame.K_e]:  # Assume 'E' key is used to open the chest
                    if self.hero.rect.colliderect(self.chests[0].rect):
                        self.healing_items.append(self.chests[0].open())
                        self.show_e_key = False

                if keys[pygame.K_h]:
                    for healing_item in self.healing_items:
                        if self.hero.rect.colliderect(healing_item.rect):
                            self.hero.heal(healing_item.healing_amount)
                            self.healing_items.remove(healing_item)
                            self.show_h_key = False


                self.enemies = [enemy for enemy in self.enemies if enemy.alive]
                if keys[pygame.K_a]:
                    self.hero.attack(self.enemies)
                for enemy in self.enemies:
                    if abs(enemy.rect.x - self.hero.rect.x) < 100:
                        enemy.attack(self.hero)
                    enemy.update(self.platforms)

                self.hero.update(keys, self.platforms)

                for enemy in self.enemies:
                    enemy.draw(self.screen)

                for platform in self.platforms:
                    platform.draw(self.screen)
                for chest in self.chests:
                    chest.draw(self.screen)
                for healing_item in self.healing_items:
                    healing_item.draw(self.screen)

                self.hero.draw(self.screen)

                # Show the key hints at the bottom of the screen
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Create an instance of the Tutorial class and run it
tutorial = Tutorial()
tutorial.run()
