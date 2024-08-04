import pygame
import sys
from tutorial import Tutorial
from level1 import Level1
from background import Background

# Define game states
TUTORIAL = "TUTORIAL"
LEVEL_1 = "LEVEL_1"
LEVEL_2 = "LEVEL_2"
LEVEL_3 = "LEVEL_3"
LEVEL_4 = "LEVEL_4"
LEVEL_5 = "LEVEL_5"
LEVEL_6 = "LEVEL_6"
LEVEL_7 = "LEVEL_7"
LEVEL_8 = "LEVEL_8"
LEVEL_9 = "LEVEL_9"
LEVEL_10 = "LEVEL_10"

class Game:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set the display mode to full screen and resizable
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)
        pygame.display.set_caption("Sword Game")

        # Load background
        self.background_tut= Background("Free-Pixel-Art-Forest/Preview/Background.png", self.screen.get_width(), self.screen.get_height())
        self.background_lvl1 = Background("ocean-and-clouds-free-pixel-art-backgrounds/Ocean_1/4.png", self.screen.get_width(), self.screen.get_height())
        # Initialize game state
        self.state = TUTORIAL

        # Create levels
        self.tutorial = Tutorial(self.screen, self.background_tut, self)

        self.level_1 = Level1(self.screen, self.background_lvl1, self, self.tutorial.hero)

        # Main game loop
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.screen.fill((255, 255, 255))  # Fill the screen with white

            if self.state == TUTORIAL:
                self.tutorial.run(keys)
            elif self.state == LEVEL_1:
                self.level_1.run(keys)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def transition_to_next_level(self):
        if self.state == TUTORIAL:
            self.state = LEVEL_1
    def transition_to_previous_level(self):
        if self.state == LEVEL_1:
            self.state = TUTORIAL
            self.tutorial.hero.rect.top = self.screen.get_height()  # Start at the top of the screen

# Create an instance of the Game class and run it
if __name__ == "__main__":
    game = Game()
    game.run()
