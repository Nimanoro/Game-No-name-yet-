import pygame
from hero import Hero
from background import Background
from golem import Golem
from plat import Platform
from chest import Chest
from key import Key
from door import Door

class Tutorial:
    def __init__(self, screen, background, game):
        self.door = Door(0, False, 350, -20, "door-art/door-1.png")
        self.screen = screen
        self.background = background
        self.game = game
        self.camera_x = 0
        self.camera_y = 0
        self.door_open = False
        self.key_picked = False
        self.key = None
        # Load key images
        self.arrow_left_image = pygame.image.load("Individual Icons/keyboard_73.png")
        self.arrow_right_image = pygame.image.load("Individual Icons/keyboard_72.png")
        self.e_key_image = pygame.image.load("Individual Icons/keyboard_15.png")
        self.h_key_image = pygame.image.load("Individual Icons/keyboard_28.png")
        self.a_key_image = pygame.image.load("Individual Icons/keyboard_23.png")
        self.arrow_up_image = pygame.image.load("Individual Icons/keyboard_70.png")
        self.w_key_image = pygame.image.load("Individual Icons/keyboard_26.png")
        self.q_key_image = pygame.image.load("Individual Icons/keyboard_16.png")



        # Transform the images to fit the screen appropriately
        key_width, key_height = 50, 50
        self.arrow_left_image = pygame.transform.scale(self.arrow_left_image, (key_width, key_height))
        self.arrow_right_image = pygame.transform.scale(self.arrow_right_image, (key_width, key_height))
        self.arrow_up_image = pygame.transform.scale(self.arrow_up_image, (key_width, key_height))
        self.a_key_image = pygame.transform.scale(self.a_key_image, (key_width, key_height))
        self.e_key_image = pygame.transform.scale(self.e_key_image, (key_width, key_height))
        self.h_key_image = pygame.transform.scale(self.h_key_image, (key_width, key_height))
        self.w_key_image = pygame.transform.scale(self.w_key_image, (key_width, key_height))
        self.q_key_image = pygame.transform.scale(self.q_key_image, (key_width, key_height))
        # Initial positions (center of the screen)
        self.left_key_initial_pos = (self.screen.get_width() // 2 - key_width - 10, self.screen.get_height() // 2)
        self.right_key_initial_pos = (self.screen.get_width() // 2 + 10, self.screen.get_height() // 2)
        self.up_key_initial_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 - key_height - 10)
        self.a_key_initial_pos = (self.screen.get_width() // 2 + 2 * key_width, self.screen.get_height() // 2)
        self.e_key_initial_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 + key_height + 20 + 10)
        self.h_key_initial_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 + key_height + 20 + 10)
        self.w_key_inital_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 + 2 * key_height + 20 + 10)
        self.q_key_initial_pos = (self.screen.get_width() // 2 - key_width // 2, self.screen.get_height() // 2 + 20 + 10)
        # Flags to control the display of key images
        self.show_e_key = False
        self.show_h_key = False
        self.show_w_key = False
        self.show_q_key = False

        # Flags to check if keys have been pressed
        self.left_key_pressed = False
        self.right_key_pressed = False
        self.up_key_pressed = False
        self.a_key_pressed = False
        self.chest_encountered = False
        self.w_key_pressed = False
        self.q_key_pressed = False
        self.key_encountered = False
        # Flags to control tutorial state
        self.tutorial_running = True

        self.platforms = [
            Platform(800, 750, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(600, 650, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(800, 495, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(600, 350, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(400, 200, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
            Platform(345, 50, 70, 30, "Platforms/Cave - Platforms-copy1.png")
        ]

        self.chests = [Chest(800, 810, "Animated Chests/Chests-1.png", "Potions/healthpotiongif.gif", 40)]
        # Create hero
        self.hero = Hero(200, 200, 5)

        self.healing_items = []
        self.enemies = [Golem(600, 760, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png", 20)]

        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True

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

        if self.tutorial_running:
            # Show the key hints in the center of the screen
            if not self.left_key_pressed:
                self.screen.blit(self.arrow_left_image, self.left_key_initial_pos)
            if not self.right_key_pressed:
                self.screen.blit(self.arrow_right_image, self.right_key_initial_pos)
            if not self.a_key_pressed:
                self.screen.blit(self.a_key_image, self.a_key_initial_pos)
            if not self.up_key_pressed:
                self.screen.blit(self.arrow_up_image, self.up_key_initial_pos)
            # Check for key presses to complete the tutorial
            if keys[pygame.K_LEFT]:
                self.left_key_pressed = True
            if keys[pygame.K_RIGHT]:
                self.right_key_pressed = True
            if keys[pygame.K_UP]:
                self.up_key_pressed = True
            if keys[pygame.K_a]:
                self.a_key_pressed = True

            # Resume the game if all tutorial keys have been pressed
            if self.left_key_pressed and self.right_key_pressed and self.a_key_pressed and self.up_key_pressed:
                self.tutorial_running = False
        else:
            # Update and draw game elements
            if self.hero.rect.colliderect(self.chests[0].rect) and not self.chest_encountered:
                self.show_e_key = True
                self.chest_encountered = True
            for chest in self.chests:
                if self.hero.rect.colliderect(chest) and self.show_e_key:
                    self.screen.blit(self.e_key_image, self.e_key_initial_pos) 

            if self.key and self.hero.rect.colliderect(self.key.rect) and not self.key_encountered:
                self.show_w_key = True
                self.key_encountered = True
            
            if self.hero.rect.colliderect(self.door.rect) and not self.q_key_pressed:
                self.show_q_key = True
            
            if self.show_q_key:
                self.screen.blit(self.q_key_image, self.q_key_initial_pos)
            
            if  self.hero.rect.colliderect(self.door.rect) and keys[pygame.K_q]:
                self.door_open = self.door.open_door(self.hero)

                

            if self.show_w_key and self.hero.rect.colliderect(self.key.rect):
                self.screen.blit(self.w_key_image, self.w_key_inital_pos)

            if self.key and keys[pygame.K_w] and self.hero.rect.colliderect(self.key.rect):
                self.hero.pick_key(self.key)
                self.key_picked = True
                self.show_w_key = False
            for healing_item in self.healing_items:
                if self.hero.rect.colliderect(healing_item.rect):
                    self.show_h_key = True
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
            if len(self.enemies) == 0 and self.key == None:
                self.key = Key("tutorial",0,  self.hero.rect.x, self.hero.rect.y, "Pixel Art Key Pack - Animated/Key 1/Key 1 - BRONZE -.png")
            if keys[pygame.K_a]:
                self.hero.attack(self.enemies)
            for enemy in self.enemies:
                if abs(enemy.rect.x - self.hero.rect.x) < 100:
                    enemy.attack(self.hero)
                enemy.update(self.platforms)

            self.hero.update(keys, self.platforms)

            # Adjust positions of game elements based on camera
            self.door.draw(self.screen, self.camera_x, self.camera_y)
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera_x, self.camera_y)
            for platform in self.platforms:
                platform.draw(self.screen, self.camera_x, self.camera_y)
            for chest in self.chests:
                chest.draw(self.screen, self.camera_x, self.camera_y)
            for healing_item in self.healing_items:
                healing_item.draw(self.screen, self.camera_x, self.camera_y)
            
            if self.key != None:
                if self.key_picked == False:
                    self.key.draw(self.screen, self.camera_x, self.camera_y)

            self.hero.draw(self.screen, self.camera_x, self.camera_y)

            # Check if hero has moved out of the screen boundaries
            if self.door_open and self.hero.rect.top < 0:
                self.game.transition_to_next_level()
            elif self.hero.rect.bottom > self.screen.get_height():
                self.game.transition_to_previous_level()

        pygame.display.flip()
        self.clock.tick(60)

    pygame.quit()
