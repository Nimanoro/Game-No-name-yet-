import pygame
import sys
from hero import Hero
from background import Background
from enemy import Enemy
from golem import Golem
from plat import Platform
from chest import Chest

# Initialize Pygame
pygame.init()

# Set the display mode to full screen and resizable
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
pygame.display.set_caption("Sword Game")

# Load background
background = Background("Free-Pixel-Art-Forest/Preview/Background.png", screen.get_width(), screen.get_height())

# Load key images

arrow_left_image = pygame.image.load("Individual Icons/keyboard_73.png")
arrow_right_image = pygame.image.load("Individual Icons/keyboard_72.png")
e_key_image = pygame.image.load("Individual Icons/keyboard_15.png")
h_key_image = pygame.image.load("Individual Icons/keyboard_28.png")


# Transform the images to fit the screen appropriately
key_width, key_height = 50, 50
arrow_left_image = pygame.transform.scale(arrow_left_image, (key_width, key_height))
arrow_right_image = pygame.transform.scale(arrow_right_image, (key_width, key_height))
e_key_image = pygame.transform.scale(e_key_image, (key_width, key_height))

# Initial positions (center of the screen)
left_key_initial_pos = (screen.get_width() // 2 - key_width - 10, screen.get_height() // 2)
right_key_initial_pos = (screen.get_width() // 2 + 10, screen.get_height() // 2)
e_key_initial_pos = (screen.get_width() // 2 - key_width // 2, screen.get_height() // 2 + key_height + 10)

# Final positions (bottom of the screen)
left_key_final_pos = (100, screen.get_height() - key_height - 10)
right_key_final_pos = (160, screen.get_height() - key_height - 10)
e_key_final_pos = (220, screen.get_height() - key_height - 10)

# Flags to control the display of key images
show_left_arrow = True
show_right_arrow = True
show_e_key = False

# Flags to check if keys have been pressed
left_key_pressed = False
right_key_pressed = False
chest_encountered = False

platforms = [
    Platform(400, 640, 100, 30, "Platforms/Cave - Platforms-copy1.png"),
    Platform(200, 480, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
    Platform(100, 350, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
    Platform(250, 250, 50, 30, "Platforms/Cave - Platforms-copy1.png"),
    Platform(500, 150, 800, 30, "Platforms/Cave - Platforms-copy1.png"),
    Platform(800, 750, 50, 30, "Platforms/Cave - Platforms-copy1.png")
]

chests = [Chest(800, 75, "Animated Chests/Chests-1.png", "Potions/healthpotiongif.gif", 40)]
# Create hero and enemy
hero = Hero(200, 820, 5)
enemies = [
    Golem(400, 50, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png"),
    Golem(700, 50, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png"),
    Golem(700, 760, 2, "/Users/nima/Game-No-name-yet-/Golem_1/Blue/No_Swoosh_VFX/attack/Golem_1_attack-1.png")
]

healing_items = []

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        left_key_pressed = True
    if keys[pygame.K_RIGHT]:
        right_key_pressed = True

    if keys[pygame.K_e]:  # Assume 'E' key is used to open the chest
        if hero.rect.colliderect(chests[0].rect):
            healing_items.append(chests[0].open())
            show_e_key = False

    if keys[pygame.K_h]:
        for healing_item in healing_items:
            if hero.rect.colliderect(healing_item.rect):
                hero.heal(healing_item.healing_amount)
                healing_items.remove(healing_item)

    chests = [chest for chest in chests if not chest.opened]

    enemies = [enemy for enemy in enemies if enemy.alive]
    if keys[pygame.K_SPACE]:
        hero.attack(enemies)
    for enemy in enemies:
        if abs(enemy.rect.x - hero.rect.x) < 100:
            enemy.attack(hero)
        enemy.update(platforms)

    hero.update(keys, platforms)
    screen.fill((255, 255, 255))  # Fill the screen with white
    background.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    for platform in platforms:
        platform.draw(screen)
    for chest in chests:
        chest.draw(screen)
    for healing_item in healing_items:
        healing_item.draw(screen)

    hero.draw(screen)

    # Show and move the key hints
    if show_left_arrow:
        if left_key_pressed:
            screen.blit(arrow_left_image, left_key_final_pos)
        else:
            screen.blit(arrow_left_image, left_key_initial_pos)

    if show_right_arrow:
        if right_key_pressed:
            screen.blit(arrow_right_image, right_key_final_pos)
        else:
            screen.blit(arrow_right_image, right_key_initial_pos)

    if hero.rect.colliderect(chests[0].rect) and not chest_encountered:
        show_e_key = True
        chest_encountered = True

    if show_e_key:
        screen.blit(e_key_image, e_key_initial_pos)
        if keys[pygame.K_e]:
            show_e_key = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


