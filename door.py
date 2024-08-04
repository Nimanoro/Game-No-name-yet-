import pygame

class Door:
    def __init__(self, number, status, x, y, image_path):
        self.number = number
        self.status = status
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image_closed = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image_closed.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image_open = pygame.transform.scale(pygame.image.load("door-art/door-2.png").convert_alpha(), (self.image.get_width() * 2, self.image.get_height() * 2))

    def open_door(self, hero):
        for key in hero.keys:
            if key.lvl == self.number:
                self.status = True
                print("Door opened")
                hero.remove_key(key)
                return True
        
            else:
                print("Door not opened")
                return False
    
    def draw(self, screen, camera_x, camera_y):
        if self.status == False:
            screen.blit(self.image_closed, (self.rect.x - camera_x, self.rect.y - camera_y))
        else:
            screen.blit(self.image_open, (self.rect.x - camera_x, self.rect.y - camera_y))

   

